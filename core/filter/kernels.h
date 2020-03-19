/* Copyright (c) 2008-2019 the MRtrix3 contributors.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * Covered Software is provided under this License on an "as is"
 * basis, without warranty of any kind, either expressed, implied, or
 * statutory, including, without limitation, warranties that the
 * Covered Software is free of defects, merchantable, fit for a
 * particular purpose or non-infringing.
 * See the Mozilla Public License v. 2.0 for more details.
 *
 * For more details, see http://www.mrtrix.org/.
 */

#ifndef __image_filter_kernels_h__
#define __image_filter_kernels_h__

#include "adapter/base.h"

namespace MR
{
  namespace Filter
  {
    namespace Kernels
    {


      using kernel_type = vector<default_type>;

      extern const kernel_type identity;
      extern const kernel_type laplacian;
      extern const kernel_type sharpen;

      extern const kernel_type sobel_x;
      extern const kernel_type sobel_y;
      extern const kernel_type sobel_z;

      extern const kernel_type sobel_feldman_x;
      extern const kernel_type sobel_feldman_y;
      extern const kernel_type sobel_feldman_z;



    }
  }
}

#endif
