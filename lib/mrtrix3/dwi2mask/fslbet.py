# Copyright (c) 2008-2019 the MRtrix3 contributors.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Covered Software is provided under this License on an "as is"
# basis, without warranty of any kind, either expressed, implied, or
# statutory, including, without limitation, warranties that the
# Covered Software is free of defects, merchantable, fit for a
# particular purpose or non-infringing.
# See the Mozilla Public License v. 2.0 for more details.
#
# For more details, see http://www.mrtrix.org/.

import os
from mrtrix3 import MRtrixError
from mrtrix3 import app, fsl, image, path, run



def usage(base_parser, subparsers): #pylint: disable=unused-variable
  parser = subparsers.add_parser('fslbet', parents=[base_parser])
  parser.set_author('Warda Syeda (wtsyeda@unimelb.edu.au) and Robert E. Smith (robert.smith@florey.edu.au)')
  parser.set_synopsis('Use the FSL Brain Extraction Tool (bet) to generate a brain mask')
  parser.add_citation('Smith, S. M. Fast robust automated brain extraction. Human Brain Mapping, 2002, 17, 143-155', is_external=True)
  parser.add_argument('input',  help='The input DWI series')
  parser.add_argument('output', help='The output mask image')
  options = parser.add_argument_group('Options specific to the \'fslbet\' algorithm')
  options.add_argument('-bet_f', type=float, help='Fractional intensity threshold (0->1); smaller values give larger brain outline estimates')
  options.add_argument('-bet_g', type=float, help='Vertical gradient in fractional intensity threshold (-1->1); positive values give larger brain outline at bottom, smaller at top')
  options.add_argument('-bet_c', metavar='<x y z>', help='Centre-of-gravity (voxels not mm) of initial mesh surface')
  options.add_argument('-bet_r', type=float, help='Head radius (mm not voxels); initial surface sphere is set to half of this')
  options.add_argument('-rescale', action='store_true', help='Rescale voxel size provided to BET to 1mm isotropic; can improve results for rodent data')



def get_inputs(): #pylint: disable=unused-variable
  pass



def execute(): #pylint: disable=unused-variable
  if not os.environ.get('FSLDIR', ''):
    raise MRtrixError('Environment variable FSLDIR is not set; please run appropriate FSL configuration script')
  bet_cmd = fsl.exe_name('bet')

  # Calculating mean b=0 image for BET
  run.command('dwiextract input.mif - -bzero | '
              'mrmath - mean - -axis 3 | '
              'mrconvert - mean_bzero.nii -strides +1,+2,+3')

  # Starting brain masking using BET
  if app.ARGS.rescale:
    run.command('mrconvert mean_bzero.nii mean_bzero_rescaled.nii -vox 1,1,1')
    vox = image.Header('mean_bzero.nii').spacing()
    b0_image = 'mean_bzero_rescaled.nii'
  else:
    b0_image = 'mean_bzero.nii'

  cmd_string = bet_cmd + ' ' + b0_image + ' DWI_BET -R -m'

  if app.ARGS.bet_f is not None:
    cmd_string += ' -f ' + str(app.ARGS.f)
  if app.ARGS.bet_g is not None:
    cmd_string += ' -g ' + str(app.ARGS.g)
  if app.ARGS.bet_r is not None:
    cmd_string += ' -r ' + str(app.ARGS.r)
  if app.ARGS.bet_c is not None:
    cmd_string += ' -c ' + app.ARGS.c

  # Running BET command
  run.command(cmd_string)
  mask = fsl.find_image('DWI_BET_mask')

  strides = image.Header('input.mif').strides()[0:3]
  strides = [(abs(value) + 1 - min(abs(v) for v in strides)) * (-1 if value < 0 else 1) for value in strides]
  run.command('mrconvert ' + mask + ' ' + path.from_user(app.ARGS.output)
              + (' -vox ' + ','.join(str(value) for value in vox) if app.ARGS.rescale else '')
              + ' -strides ' + ','.join(str(value) for value in strides)
              + ' -datatype bit',
              mrconvert_keyval=path.from_user(app.ARGS.input, False),
              force=app.FORCE_OVERWRITE)
