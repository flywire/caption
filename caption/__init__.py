# caption: Manage markdown captions
#
# Copyright (c) 2020-2023 flywire
# Copyright (c) 2023 sanzoghenzo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .image_caption import ImageCaptionExtension
from .table_caption import TableCaptionExtension
from .caption import CaptionExtension

__all__ = ['ImageCaptionExtension', 'TableCaptionExtension', 'CaptionExtension']
