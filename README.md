# Matterport3D Dataset Downloader

This script downloads and extracts the Matterport3D dataset, improving download speed and automating extraction and deletion of compressed files.

该脚本用于下载和解压 Matterport3D 数据集，提高了下载速度并自动解压和删除压缩文件。

## Features / 功能

- Multithreaded downloading for improved speed.
- Automatic extraction of downloaded files.
- Deletion of compressed files after extraction to save space.
- Logging of download progress and errors.

- 多线程下载以提高速度。
- 自动解压下载的文件。
- 解压后删除压缩文件以节省空间。
- 下载进度和错误日志记录。

## Requirements / 依赖

- Python 3.6+
- `tqdm`
- `requests`

Install the required packages using:
使用以下命令安装所需的包：
```bash
pip install tqdm requests
```

## Usage / 使用方法

To download the dataset, use the following command:
使用以下命令下载数据集：
```bash
python download_mp.py -o base_dir --scans scans.txt --type object_segmentations --task_data semantic_voxel_label_data semantic_voxel_label_models
```

### Arguments / 参数

- `-o, --out_dir` (required): Directory to download the files to.
- `--scans` (required): File containing the scan IDs to download.
- `--task_data` (optional): Task data and models to download. Options: `keypoint_matching_data`, `keypoint_matching_models`, `surface_normal_data`, `surface_normal_models`, `region_classification_data`, `region_classification_models`, `semantic_voxel_label_data`, `semantic_voxel_label_models`, `minos`, `gibson`, `habitat`, `pixelsynth`, `igibson`, `mp360`.
- `--type` (optional): Specific file types to download. Options: `cameras`, `matterport_camera_intrinsics`, `matterport_camera_poses`, `matterport_color_images`, `matterport_depth_images`, `matterport_hdr_images`, `matterport_mesh`, `matterport_skybox_images`, `undistorted_camera_parameters`, `undistorted_color_images`, `undistorted_depth_images`, `undistorted_normal_images`, `house_segmentations`, `region_segmentations`, `image_overlap_data`, `poisson_meshes`, `sens`.
- `--log_file` (optional): Path to the log file. Default is `download.log`.

- `-o, --out_dir` (必需): 下载文件的目录。
- `--scans` (必需): 包含要下载的扫描ID的文件。
- `--task_data` (可选): 要下载的任务数据和模型。选项：`keypoint_matching_data`, `keypoint_matching_models`, `surface_normal_data`, `surface_normal_models`, `region_classification_data`, `region_classification_models`, `semantic_voxel_label_data`, `semantic_voxel_label_models`, `minos`, `gibson`, `habitat`, `pixelsynth`, `igibson`, `mp360`.
- `--type` (可选): 要下载的特定文件类型。选项：`cameras`, `matterport_camera_intrinsics`, `matterport_camera_poses`, `matterport_color_images`, `matterport_depth_images`, `matterport_hdr_images`, `matterport_mesh`, `matterport_skybox_images`, `undistorted_camera_parameters`, `undistorted_color_images`, `undistorted_depth_images`, `undistorted_normal_images`, `house_segmentations`, `region_segmentations`, `image_overlap_data`, `poisson_meshes`, `sens`.
- `--log_file` (可选): 日志文件的路径。默认为 `download.log`。

### Example / 示例

To download all available data types for scans listed in `scans.txt` to the directory `base_dir`, and also download the `semantic_voxel_label_data` and `semantic_voxel_label_models`, use:
要将 `scans.txt` 中列出的所有数据类型下载到目录 `base_dir`，并下载 `semantic_voxel_label_data` 和 `semantic_voxel_label_models`，请使用以下命令：

```bash
python download_mp.py -o base_dir --scans scans.txt --task_data semantic_voxel_label_data semantic_voxel_label_models
```

### Logging / 日志

Logs are stored in the specified log file (`download.log` by default). The log includes timestamps and details about each download step, including any errors encountered.
日志记录在指定的日志文件中（默认为 `download.log`）。日志包括时间戳和每个下载步骤的详细信息，包括遇到的任何错误。

## Terms of Service / 服务条款

By using this script, you agree to the Matterport3D Terms of Service available at:
使用此脚本即表示您同意 Matterport3D 服务条款，详情见：
[MP Terms of Service / MP 服务条款](http://kaldir.vc.in.tum.de/matterport/MP_TOS.pdf)

**Important: Please ensure you have obtained permission from Matterport before downloading the dataset.**
**重要提示：在下载数据集之前，请确保您已获得 Matterport 的许可。**

## License / 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
此项目依据 MIT 许可证进行许可 - 详情参见 [LICENSE](LICENSE) 文件。

## Contributing / 贡献

Contributions are welcome! Please feel free to submit a Pull Request.
欢迎贡献！请随时提交 Pull Request。

## Acknowledgments / 鸣谢

This script is based on the original Matterport3D dataset download script, with modifications for improved speed and functionality.
此脚本基于原始 Matterport3D 数据集下载脚本进行修改，以提高速度和功能。
