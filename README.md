# Matterport3D Dataset Downloader

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/wtzmx/Matterport3D-Dataset-Downloader/issues)
[![Downloads](https://img.shields.io/github/downloads/wtzmx/Matterport3D-Dataset-Downloader/total.svg)](https://github.com/wtzmx/Matterport3D-Dataset-Downloader/releases)

A high-performance downloader for the Matterport3D dataset, featuring multi-threaded downloading, automatic extraction, and space optimization.

## ✨ Features

- 🚀 Multi-threaded downloading for improved speed
- 📦 Automatic extraction of downloaded files
- 💾 Space optimization through automatic cleanup of compressed files
- 📝 Comprehensive logging of download progress and errors

## 🔧 Requirements

- Python 3.6+
- Required packages:
  ```bash
  pip install tqdm requests
  ```

## 🚀 Quick Start

```bash
python download_mp.py -o base_dir --scans scans.txt --type object_segmentations --task_data semantic_voxel_label_data semantic_voxel_label_models
```

## 📖 Usage

### Command Line Arguments

| Argument | Required | Description | Options |
|----------|----------|-------------|----------|
| `-o, --out_dir` | ✅ | Download directory | Path to output directory |
| `--scans` | ✅ | Scan IDs file | Path to file containing scan IDs |
| `--task_data` | ❌ | Task data and models | `keypoint_matching_data`, `keypoint_matching_models`, `surface_normal_data`, `surface_normal_models`, etc. |
| `--type` | ❌ | File types | `cameras`, `matterport_camera_intrinsics`, `matterport_color_images`, etc. |
| `--log_file` | ❌ | Log file path | Default: `download.log` |

### Available Task Data Options
- `keypoint_matching_data`
- `keypoint_matching_models`
- `surface_normal_data`
- `surface_normal_models`
- `region_classification_data`
- `region_classification_models`
- `semantic_voxel_label_data`
- `semantic_voxel_label_models`
- `minos`
- `gibson`
- `habitat`
- `pixelsynth`
- `igibson`
- `mp360`

### Available File Types
- `cameras`
- `matterport_camera_intrinsics`
- `matterport_camera_poses`
- `matterport_color_images`
- `matterport_depth_images`
- `matterport_hdr_images`
- `matterport_mesh`
- `matterport_skybox_images`
- `undistorted_camera_parameters`
- `undistorted_color_images`
- `undistorted_depth_images`
- `undistorted_normal_images`
- `house_segmentations`
- `region_segmentations`
- `image_overlap_data`
- `poisson_meshes`
- `sens`

### Example Usage

Download all available data types for specified scans with additional task data:
```bash
python download_mp.py -o base_dir --scans scans.txt --task_data semantic_voxel_label_data semantic_voxel_label_models
```

## 📝 Logging

- Default log file: `download.log`
- Logs include:
  - Timestamps
  - Download progress
  - Extraction status
  - Error messages
  - Cleanup confirmations

## ⚠️ Important Notice

Before using this downloader, you must:
1. Obtain permission from Matterport
2. Agree to the [Matterport3D Terms of Service](http://kaldir.vc.in.tum.de/matterport/MP_TOS.pdf)
3. Have sufficient storage space for downloaded data

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Submit issues
- Create pull requests
- Suggest improvements
- Report bugs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Based on the original Matterport3D dataset download script, enhanced with additional features for improved performance and user experience.
