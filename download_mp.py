import argparse
import os
import tempfile
import urllib.request
import time
import zipfile
import logging
import shutil
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = 'http://kaldir.vc.in.tum.de/matterport/'
RELEASE = 'v1/scans'
RELEASE_TASKS = 'v1/tasks/'
RELEASE_SIZE = '1.3TB'
TOS_URL = BASE_URL + 'MP_TOS.pdf'
FILETYPES = [
    'cameras',
    'matterport_camera_intrinsics',
    'matterport_camera_poses',
    'matterport_color_images',
    'matterport_depth_images',
    'matterport_hdr_images',
    'matterport_mesh',
    'matterport_skybox_images',
    'undistorted_camera_parameters',
    'undistorted_color_images',
    'undistorted_depth_images',
    'undistorted_normal_images',
    'house_segmentations',
    'region_segmentations',
    'image_overlap_data',
    'poisson_meshes',
    'sens'
]
TASK_FILES = {
    'keypoint_matching_data': ['keypoint_matching/data.zip'],
    'keypoint_matching_models': ['keypoint_matching/models.zip'],
    'surface_normal_data': ['surface_normal/data_list.zip'],
    'surface_normal_models': ['surface_normal/models.zip'],
    'region_classification_data': ['region_classification/data.zip'],
    'region_classification_models': ['region_classification/models.zip'],
    'semantic_voxel_label_data': ['semantic_voxel_label/data.zip'],
    'semantic_voxel_label_models': ['semantic_voxel_label/models.zip'],
    'minos': ['mp3d_minos.zip'],
    'gibson': ['mp3d_for_gibson.tar.gz'],
    'habitat': ['mp3d_habitat.zip'],
    'pixelsynth': ['mp3d_pixelsynth.zip'],
    'igibson': ['mp3d_for_igibson.zip'],
    'mp360': ['mp3d_360/data_00.zip', 'mp3d_360/data_01.zip', 'mp3d_360/data_02.zip', 'mp3d_360/data_03.zip', 'mp3d_360/data_04.zip', 'mp3d_360/data_05.zip', 'mp3d_360/data_06.zip']
}

def setup_logging(log_file):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 创建文件处理器
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # 创建格式器并将其添加到处理器中
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # 将处理器添加到记录器中
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

def get_scans_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            scans = [line.strip() for line in file.readlines()]
        return scans
    except Exception as e:
        logging.error(f"Error reading {file_path}: {e}")
        return []

def download_release(release_scans, out_dir, file_types):
    logging.info(f'开始下载 MP 发布到 {out_dir}...')
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(download_scan, scan_id, out_dir, file_types)
            for scan_id in release_scans
        ]
        for future in as_completed(futures):
            future.result()
    logging.info('MP 发布下载完成。')

def download_file(url, out_file):
    out_dir = os.path.dirname(out_file)
    if not os.path.isfile(out_file):
        fh, out_file_tmp = tempfile.mkstemp(dir=out_dir)
        f = os.fdopen(fh, 'w')
        f.close()
        start_time = time.time()
        with urllib.request.urlopen(url) as response, open(out_file_tmp, 'wb') as out_file_handle:
            file_size = int(response.getheader('Content-Length'))
            chunk_size = 1024
            with tqdm(total=file_size, unit='B', unit_scale=True, desc=os.path.basename(out_file), ncols=80, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]') as pbar:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    out_file_handle.write(chunk)
                    pbar.update(len(chunk))
        os.rename(out_file_tmp, out_file)
        end_time = time.time()
        download_time = end_time - start_time
        download_speed = file_size / download_time / 1024
        pbar.set_postfix_str(f'{download_speed:.2f} KB/s')
        logging.info(f'下载完成: {out_file}, 用时: {download_time:.2f}秒, 速度: {download_speed:.2f} KB/s')
        unzip_file(out_file)
    else:
        logging.info(f'文件已存在，跳过下载: {out_file}')
        unzip_file(out_file)

def download_scan(scan_id, out_dir, file_types):
    logging.info(f'开始下载 MP 扫描 {scan_id} ...')
    scan_out_dir = os.path.join(out_dir, scan_id)
    if not os.path.isdir(scan_out_dir):
        os.makedirs(scan_out_dir)
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(download_file, BASE_URL + RELEASE + '/' + scan_id + '/' + ft + '.zip', os.path.join(scan_out_dir, ft + '.zip'))
            for ft in file_types
        ]
        for future in as_completed(futures):
            future.result()
    logging.info(f'扫描下载完成 {scan_id}')

def download_task_data(task_data, out_dir):
    logging.info(f'开始下载 MP 任务数据 {str(task_data)} ...')
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for task_data_id in task_data:
            if task_data_id in TASK_FILES:
                for filepart in TASK_FILES[task_data_id]:
                    url = BASE_URL + RELEASE_TASKS + '/' + filepart
                    localpath = os.path.join(out_dir, filepart)
                    localdir = os.path.dirname(localpath)
                    if not os.path.isdir(localdir):
                        os.makedirs(localdir)
                    futures.append(executor.submit(download_file, url, localpath))
        for future in as_completed(futures):
            future.result()
    logging.info(f'任务数据下载完成 {str(task_data)}')

def unzip_file(file_path):
    if zipfile.is_zipfile(file_path):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            extract_dir = os.path.dirname(os.path.dirname(file_path))  # 设置解压路径到上一级目录，即 scans 文件夹
            zip_ref.extractall(extract_dir)
        logging.info(f'解压完成: {file_path}')
        # 删除压缩包
        try:
            os.remove(file_path)
            logging.info(f'删除压缩包: {file_path}')
        except OSError as e:
            logging.error(f'删除压缩包失败: {file_path}, 错误: {e}')
    else:
        logging.warning(f'文件不是ZIP格式，跳过解压: {file_path}')



def main():
    parser = argparse.ArgumentParser(description=
        '''
        下载 MP 公共数据发布。
        示例调用：
          python download_mp.py -o base_dir --scans scans.txt --type object_segmentations --task_data semantic_voxel_label_data semantic_voxel_label_models
        -o 参数是必需的，指定本地目录 base_dir。
        下载后 base_dir/v1/scans 将填充扫描数据，base_dir/v1/tasks 将填充任务数据。
        从 base_dir/v1/scans 中解压扫描文件，从 base_dir/v1/tasks/task_name 中解压任务文件。
        --type 参数是可选的（如果未指定，则下载所有数据类型）。
        --scans 参数指定要下载的扫描ID文件。
        --task_data 参数是可选的，将下载任务数据和模型文件。
        ''',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-o', '--out_dir', required=True, help='下载到的目录')
    parser.add_argument('--scans', required=True, help='包含扫描ID的文件')
    parser.add_argument('--task_data', default=[], nargs='+', help='要下载的任务数据文件。任意一个：' + ','.join(TASK_FILES.keys()))
    parser.add_argument('--type', nargs='+', help='要下载的特定文件类型。任意一个：' + ','.join(FILETYPES))
    parser.add_argument('--log_file', default='download.log', help='日志文件路径')
    args = parser.parse_args()

    setup_logging(args.log_file)

    logging.info('按任意键继续确认您已同意 MP 使用条款，如下所述：')
    logging.info(TOS_URL)
    logging.info('***')
    input('按任意键继续，或按 CTRL-C 退出。')

    release_scans = get_scans_from_file(args.scans)
    if not release_scans:
        logging.error(f"未能读取扫描ID列表，请检查文件路径和内容: {args.scans}")
        return

    logging.info(f"本次共下载 {len(release_scans)} 个房间数据，是否确认下载？ (y/n)")
    confirm = input().strip().lower()
    if confirm != 'y':
        logging.info("取消下载。")
        return

    file_types = FILETYPES

    # 下载任务数据
    if args.task_data:
        if set(args.task_data) & set(TASK_FILES.keys()):  # 下载任务数据
            out_dir = os.path.join(args.out_dir, RELEASE_TASKS)
            download_task_data(args.task_data, out_dir)
        else:
            logging.error('错误：无法识别的任务数据 ID：' + str(args.task_data))
            input('按任意键继续下载主数据集，或按 CTRL-C 退出。')

    # 下载特定文件类型？
    if args.type:
        if not set(args.type) & set(FILETYPES):
            logging.error('错误：无效的文件类型：' + str(args.type))
            return
        file_types = args.type

    out_dir = os.path.join(args.out_dir, RELEASE)
    download_release(release_scans, out_dir, file_types)

if __name__ == "__main__":
    main()
