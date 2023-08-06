# Copyright (c) 2022 NVIDIA CORPORATION.  All rights reserved.
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import os

version = "0.5.0"

cuda_path = None        # path to local CUDA toolchain, if None at init time warp will attempt to find the SDK using CUDA_PATH env var

verify_fp = False       # verify inputs and outputs are finite after each launch
verify_cuda = False     # if true will check CUDA errors after each kernel launch / memory operation
print_launches = False  # if true will print out launch information

enable_backward = False # disable code gen of backwards pass

mode = "release"
verbose = False

host_compiler = None    # user can specify host compiler here, otherwise will attempt to find one automatically

cache_kernels = True
kernel_cache_dir = None # path to kernel cache directory, if None a default path will be used

ptx_target_arch = 70    # target architecture for PTX generation, defaults to the lowest architecture that supports all of Warp's features
