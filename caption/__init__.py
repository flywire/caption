# caption: Manage markdown captions
#
# Copyright (c) 2020-2023 flywire
# Copyright (c) 2023 sanzoghenzo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .caption import makeExtension, CaptionExtension
from .image_caption import ImageCaptionExtension

__all__ = ['makeExtension', 'CaptionExtension']
