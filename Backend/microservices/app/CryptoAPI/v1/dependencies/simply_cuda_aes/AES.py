'''
This file contains the best performing AES encryption implementation and corresponding
decryption implementation, and the helper functions to easily encrypt and decrypt files
using this class by running this script. 
'''

import numpy as np
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import pycuda.autoinit
import secrets

import sys
import os

class AES:
    def __init__(self):


        self.get_source_module_encrypt()
        self.get_source_module_decrypt()

        self.sbox = np.array([
            0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    	    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    	    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    	    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    	    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    	    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    	    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    	    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    	    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    	    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    	    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    	    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    	    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    	    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    	    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    	    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
        ], dtype=np.byte)
        
        self.invSbox = np.array([
            0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
            0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
            0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
            0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
            0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
            0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
            0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
            0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
            0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
            0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
            0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
            0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
            0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
            0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
            0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
            0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D, 
        ], dtype=np.byte)


        self.rcon = np.array([
            0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
    	    0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39,
    	    0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a,
    	    0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,
    	    0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,
    	    0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc,
        	0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b,
        	0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
        	0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94,
        	0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20,
        	0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,
        	0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f,
        	0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
        	0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63,
        	0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd,
        	0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d
        ], dtype=np.byte)

        self.mul2 = np.array([
            0x00, 0x02, 0x04, 0x06, 0x08, 0x0a, 0x0c, 0x0e, 0x10, 0x12, 0x14, 0x16, 0x18, 0x1a, 0x1c, 0x1e,
        	0x20, 0x22, 0x24, 0x26, 0x28, 0x2a, 0x2c, 0x2e, 0x30, 0x32, 0x34, 0x36, 0x38, 0x3a, 0x3c, 0x3e,
        	0x40, 0x42, 0x44, 0x46, 0x48, 0x4a, 0x4c, 0x4e, 0x50, 0x52, 0x54, 0x56, 0x58, 0x5a, 0x5c, 0x5e,
        	0x60, 0x62, 0x64, 0x66, 0x68, 0x6a, 0x6c, 0x6e, 0x70, 0x72, 0x74, 0x76, 0x78, 0x7a, 0x7c, 0x7e,
        	0x80, 0x82, 0x84, 0x86, 0x88, 0x8a, 0x8c, 0x8e, 0x90, 0x92, 0x94, 0x96, 0x98, 0x9a, 0x9c, 0x9e,
        	0xa0, 0xa2, 0xa4, 0xa6, 0xa8, 0xaa, 0xac, 0xae, 0xb0, 0xb2, 0xb4, 0xb6, 0xb8, 0xba, 0xbc, 0xbe,
        	0xc0, 0xc2, 0xc4, 0xc6, 0xc8, 0xca, 0xcc, 0xce, 0xd0, 0xd2, 0xd4, 0xd6, 0xd8, 0xda, 0xdc, 0xde,
        	0xe0, 0xe2, 0xe4, 0xe6, 0xe8, 0xea, 0xec, 0xee, 0xf0, 0xf2, 0xf4, 0xf6, 0xf8, 0xfa, 0xfc, 0xfe,
        	0x1b, 0x19, 0x1f, 0x1d, 0x13, 0x11, 0x17, 0x15, 0x0b, 0x09, 0x0f, 0x0d, 0x03, 0x01, 0x07, 0x05,
        	0x3b, 0x39, 0x3f, 0x3d, 0x33, 0x31, 0x37, 0x35, 0x2b, 0x29, 0x2f, 0x2d, 0x23, 0x21, 0x27, 0x25,
        	0x5b, 0x59, 0x5f, 0x5d, 0x53, 0x51, 0x57, 0x55, 0x4b, 0x49, 0x4f, 0x4d, 0x43, 0x41, 0x47, 0x45,
        	0x7b, 0x79, 0x7f, 0x7d, 0x73, 0x71, 0x77, 0x75, 0x6b, 0x69, 0x6f, 0x6d, 0x63, 0x61, 0x67, 0x65,
        	0x9b, 0x99, 0x9f, 0x9d, 0x93, 0x91, 0x97, 0x95, 0x8b, 0x89, 0x8f, 0x8d, 0x83, 0x81, 0x87, 0x85,
        	0xbb, 0xb9, 0xbf, 0xbd, 0xb3, 0xb1, 0xb7, 0xb5, 0xab, 0xa9, 0xaf, 0xad, 0xa3, 0xa1, 0xa7, 0xa5,
        	0xdb, 0xd9, 0xdf, 0xdd, 0xd3, 0xd1, 0xd7, 0xd5, 0xcb, 0xc9, 0xcf, 0xcd, 0xc3, 0xc1, 0xc7, 0xc5,
        	0xfb, 0xf9, 0xff, 0xfd, 0xf3, 0xf1, 0xf7, 0xf5, 0xeb, 0xe9, 0xef, 0xed, 0xe3, 0xe1, 0xe7, 0xe5
        ], dtype=np.byte)

        self.mul3 = np.array([
            0x00, 0x03, 0x06, 0x05, 0x0c, 0x0f, 0x0a, 0x09, 0x18, 0x1b, 0x1e, 0x1d, 0x14, 0x17, 0x12, 0x11,
        	0x30, 0x33, 0x36, 0x35, 0x3c, 0x3f, 0x3a, 0x39, 0x28, 0x2b, 0x2e, 0x2d, 0x24, 0x27, 0x22, 0x21,
        	0x60, 0x63, 0x66, 0x65, 0x6c, 0x6f, 0x6a, 0x69, 0x78, 0x7b, 0x7e, 0x7d, 0x74, 0x77, 0x72, 0x71,
        	0x50, 0x53, 0x56, 0x55, 0x5c, 0x5f, 0x5a, 0x59, 0x48, 0x4b, 0x4e, 0x4d, 0x44, 0x47, 0x42, 0x41,
        	0xc0, 0xc3, 0xc6, 0xc5, 0xcc, 0xcf, 0xca, 0xc9, 0xd8, 0xdb, 0xde, 0xdd, 0xd4, 0xd7, 0xd2, 0xd1,
        	0xf0, 0xf3, 0xf6, 0xf5, 0xfc, 0xff, 0xfa, 0xf9, 0xe8, 0xeb, 0xee, 0xed, 0xe4, 0xe7, 0xe2, 0xe1,
        	0xa0, 0xa3, 0xa6, 0xa5, 0xac, 0xaf, 0xaa, 0xa9, 0xb8, 0xbb, 0xbe, 0xbd, 0xb4, 0xb7, 0xb2, 0xb1,
        	0x90, 0x93, 0x96, 0x95, 0x9c, 0x9f, 0x9a, 0x99, 0x88, 0x8b, 0x8e, 0x8d, 0x84, 0x87, 0x82, 0x81,
        	0x9b, 0x98, 0x9d, 0x9e, 0x97, 0x94, 0x91, 0x92, 0x83, 0x80, 0x85, 0x86, 0x8f, 0x8c, 0x89, 0x8a,
        	0xab, 0xa8, 0xad, 0xae, 0xa7, 0xa4, 0xa1, 0xa2, 0xb3, 0xb0, 0xb5, 0xb6, 0xbf, 0xbc, 0xb9, 0xba,
        	0xfb, 0xf8, 0xfd, 0xfe, 0xf7, 0xf4, 0xf1, 0xf2, 0xe3, 0xe0, 0xe5, 0xe6, 0xef, 0xec, 0xe9, 0xea,
        	0xcb, 0xc8, 0xcd, 0xce, 0xc7, 0xc4, 0xc1, 0xc2, 0xd3, 0xd0, 0xd5, 0xd6, 0xdf, 0xdc, 0xd9, 0xda,
        	0x5b, 0x58, 0x5d, 0x5e, 0x57, 0x54, 0x51, 0x52, 0x43, 0x40, 0x45, 0x46, 0x4f, 0x4c, 0x49, 0x4a,
        	0x6b, 0x68, 0x6d, 0x6e, 0x67, 0x64, 0x61, 0x62, 0x73, 0x70, 0x75, 0x76, 0x7f, 0x7c, 0x79, 0x7a,
        	0x3b, 0x38, 0x3d, 0x3e, 0x37, 0x34, 0x31, 0x32, 0x23, 0x20, 0x25, 0x26, 0x2f, 0x2c, 0x29, 0x2a,
        	0x0b, 0x08, 0x0d, 0x0e, 0x07, 0x04, 0x01, 0x02, 0x13, 0x10, 0x15, 0x16, 0x1f, 0x1c, 0x19, 0x1a
        ], dtype=np.byte)


    def get_source_module_encrypt(self):
        main_pth = os.path.dirname(os.path.abspath(__file__))

        private_sharedlut = """
        #define AES_PRIVATESTATE_SHAREDLUT
        #define LUT_IN_SHARED
        """

        file = open(main_pth + "/kernels/general.cuh", "r")
        kernelwrapper = file.read()
        file.close()
        file = open(main_pth + "/kernels/SubBytes.cuh", "r")
        kernelwrapper += file.read()
        file.close()
        file = open(main_pth + "/kernels/ShiftRows.cuh", "r")
        kernelwrapper += file.read()
        file.close()
        file = open(main_pth + "/kernels/MixColumns.cuh", "r")
        kernelwrapper += file.read()
        file.close()
        file = open(main_pth + "/kernels/AddRoundKey.cuh", "r")
        kernelwrapper += file.read()
        file.close()
        file = open(main_pth + "/kernels/Round.cuh", "r")
        kernelwrapper += file.read()
        file.close()
        file = open(main_pth + "/kernels/KeyExpansion.cuh", "r")
        kernelwrapper += file.read()
        file.close()
        file = open(main_pth + "/kernels/FinalRound.cuh", "r")
        kernelwrapper += file.read()
        file.close()
        file = open(main_pth + "/kernels/AES.cuh", "r")
        kernelwrapper += file.read()
        file.close()

        self.module_encrypt = SourceModule(private_sharedlut + kernelwrapper)

    def get_source_module_decrypt(self):
        main_pth = os.path.dirname(os.path.abspath(__file__))
        sharedLut = """
        #define LUT_IN_SHARED
        """

        with open(main_pth + "/kernels/general.cuh", "r") as f:
            kernelwrapper = f.read()
        with open(main_pth + "/kernels/InvSubbytes.cuh", "r") as f:
            kernelwrapper += f.read()
        with open(main_pth + "/kernels/InvShiftRows.cuh", "r") as f:
            kernelwrapper += f.read()
        with open(main_pth + "/kernels/MixColumns.cuh", "r") as f: # inv Mix Columns depends on mix Columns!
            kernelwrapper += f.read()
        with open(main_pth + "/kernels/InvMixColumns.cuh", "r") as f:
            kernelwrapper += f.read()
        with open(main_pth + "/kernels/AddRoundKey.cuh", "r") as f:
            kernelwrapper += f.read()
        with open(main_pth + "/kernels/InvRound.cuh", "r") as f:
            kernelwrapper += f.read()
        with open(main_pth + "/kernels/KeyExpansion.cuh", "r") as f:
            kernelwrapper += f.read()
        with open(main_pth + "/kernels/InvFinalRound.cuh", "r") as f:
            kernelwrapper += f.read()
        with open(main_pth + "/kernels/InvAES.cuh", "r") as f:
            kernelwrapper += f.read()

        self.module_decrpyt = SourceModule(sharedLut + kernelwrapper)


    def encrypt_gpu(self, state, cipherkey, statelength, block_size=None):
        # Pad the message so its length is a multiple of 16 bytes
        if (statelength % 16 != 0):
            padding = np.zeros(16 - statelength % 16, state.dtype)
            state = np.append(state, padding)
            statelength += 16 - statelength % 16

        # Device memory allocation for input and output arrays
        io_state_gpu = cuda.mem_alloc_like(state)
        i_cipherkey_gpu = cuda.mem_alloc_like(cipherkey)
        i_rcon_gpu = cuda.mem_alloc_like(self.rcon)
        i_sbox_gpu = cuda.mem_alloc_like(self.sbox)
        i_mul2_gpu = cuda.mem_alloc_like(self.mul2)
        i_mul3_gpu = cuda.mem_alloc_like(self.mul3)

        # Copy data from host to device
        cuda.memcpy_htod(io_state_gpu, state)
        cuda.memcpy_htod(i_cipherkey_gpu, cipherkey)
        cuda.memcpy_htod(i_rcon_gpu, self.rcon)
        cuda.memcpy_htod(i_sbox_gpu, self.sbox)
        cuda.memcpy_htod(i_mul2_gpu, self.mul2)
        cuda.memcpy_htod(i_mul3_gpu, self.mul3)

        # Calculate block size and grid size
        if block_size is None:
            block_size = (statelength - 1) // 16 + 1
            grid_size = 1
            if (block_size > 1024):
                block_size = 1024
                grid_size = (statelength - 1) // (1024 * 16) + 1
        else:
            grid_size = (statelength - 1) // (block_size * 16) + 1

        blockDim = (block_size, 1, 1)
        gridDim = (grid_size, 1, 1)

        # call kernel
        prg = self.module_encrypt.get_function("AES_private_sharedlut")
        prg(io_state_gpu, i_cipherkey_gpu, np.uint32(statelength), i_rcon_gpu, i_sbox_gpu, i_mul2_gpu, i_mul3_gpu, block=blockDim, grid=gridDim)

        # copy results from device to host
        res = np.empty_like(state)
        cuda.memcpy_dtoh(res, io_state_gpu)

        return res
    
    def decrypt_gpu(self, state, cipherkey, statelength, block_size=None):
        # Pad the message so its length is a multiple of 16 bytes
        if (statelength % 16 != 0):
            padding = np.zeros(16 - statelength % 16, state.dtype)
            state = np.append(state, padding)
            statelength += 16 - statelength % 16
        
        # device memory allocation
        io_state_gpu = cuda.mem_alloc_like(state)
        i_cipherkey_gpu = cuda.mem_alloc_like(cipherkey)
        i_rcon_gpu = cuda.mem_alloc_like(self.rcon)
        i_sbox_gpu = cuda.mem_alloc_like(self.sbox)
        i_invsbox_gpu = cuda.mem_alloc_like(self.invSbox)
        i_mul2_gpu = cuda.mem_alloc_like(self.mul2)
        i_mul3_gpu = cuda.mem_alloc_like(self.mul3)
        
        cuda.memcpy_htod(io_state_gpu, state)
        cuda.memcpy_htod(i_cipherkey_gpu, cipherkey)
        cuda.memcpy_htod(i_rcon_gpu, self.rcon)
        cuda.memcpy_htod(i_sbox_gpu, self.sbox)
        cuda.memcpy_htod(i_invsbox_gpu, self.invSbox)
        cuda.memcpy_htod(i_mul2_gpu, self.mul2)
        cuda.memcpy_htod(i_mul3_gpu, self.mul3)

        # Calculate block size and grid size
        if block_size is None:
            block_size = (statelength - 1) // 16 + 1
            grid_size = 1
            if (block_size > 1024):
                block_size = 1024
                grid_size = (statelength - 1) // (1024 * 16) + 1
        else:
            grid_size = (statelength - 1) // (block_size * 16) + 1

        blockDim = (block_size, 1, 1)
        gridDim = (grid_size, 1, 1)

        # call kernel
        prg = self.module_decrpyt.get_function("inv_AES")
        prg(io_state_gpu, i_cipherkey_gpu, np.uint32(statelength), i_rcon_gpu, i_sbox_gpu,  i_invsbox_gpu, i_mul2_gpu, i_mul3_gpu, block=blockDim, grid=gridDim)

        # Copy result from device to the host
        res = np.empty_like(state)
        cuda.memcpy_dtoh(res, io_state_gpu)

        return res


class CryptoGPU:

    def __init__(self, key: str) -> None:
        
        # Get random key
        self.hex_key = key if key else self.generate_secret_hex()
        self.byte_key = bytes.fromhex(self.hex_key)
        self.byte_array_key = np.frombuffer(self.byte_key, dtype=np.byte)

    @staticmethod
    def generate_secret_hex():
        return secrets.token_hex(32)

    # En pruebas
    def hidde_key(self, secret: str) -> None:
        """
        Esconde la llave en la variable de entorno, para luego en úso de producción
        tener una misma llave especifica para integrar sin hacer mas verboso el código.

        Como usarlo directo con Dokcer o tu propia PC

        Comprueba la compatibilidad de la misma clave antes de aplicarlo y esto conlleva que si
        hay algún problema lanazara un raise donde parara el código

        La variable se llama EASY_CRYPTO_CUDA_GPU_CRYPTO_GPU

        Args:
            secret (str): La clave de encriptación secreta a esconder en la variable de entorno.

        Raises:
            ValueError: Si la clave no es válida para encriptar y desencriptar 'test'.
            SystemError: Si hay un error fatal al configurar la clave en la variable de entorno.
        """
        try:
            os.environ['EASY_CRYPTO_CUDA_GPU_CRYPTO_GPU'] = str(secret)

            try:
                test_encrypt = self.encrypt('test')
                test_decypt = self.decrypt(test_encrypt)
            except Exception:
                raise ValueError("La clave no es valida para el úso")

        except Exception as e:
            raise SystemError("Hubo un error fatal al implementar y a verificar la clave de encriptación")
        
        pass

    def encrypt(self, input_bytes: bytes) -> str:

        """
        Encripta por medio de CUDA a través de la GPU Nvidia

        Args:
            input (str): Entrada de texto a encriptar
        
        Result:
            str: Texto encriptado por string
        """

        #input_bytes = input.encode('utf-8')
        byte_array_in = np.frombuffer(input_bytes, dtype=np.byte)

        computer = AES()
        
        encrypted = computer.encrypt_gpu(byte_array_in, self.byte_array_key, byte_array_in.size)
        encrypted_hex: str = bytes(encrypted).hex()
        return encrypted_hex
    

    def decrypt(self, encrypted_hex: str) -> str:

        """
        Decripta por medio de CUDA a través de la GPU Nvidia

        Args:
            input (str): Entrada de texto a decriptar
        
        Result:
            str: Texto decriptado por string
        """
        # Convertir bytes a cadena de texto hexadecimal
        if isinstance(encrypted_hex, bytes):
            hex_string = encrypted_hex.decode()
        else:
            hex_string = encrypted_hex

        #print(f"Cadena hexadecimal: {hex_string}")

        # Convertir la cadena hexadecimal a bytes
        encrypted_bytes = bytes.fromhex(hex_string)
        #print(f"Bytes decodificados: {encrypted_bytes}")

        byte_array_in = np.frombuffer(encrypted_bytes, dtype=np.byte)

        computer = AES()
        decrypted = computer.decrypt_gpu(byte_array_in, self.byte_array_key, byte_array_in.size)
        

        # Convertir resultado a string, manejando el padding si es necesario
        decrypted_bytes = bytes(decrypted)
        #print(f"Bytes desencriptados: {decrypted_bytes}")

        # Intentar decodificar
        try:
            decrypted_str = decrypted_bytes.decode('utf-8').rstrip('\x00')  # Removing potential padding
            print(decrypted_bytes)
            print(decrypted_str)
        except UnicodeDecodeError:
            # Manejo de errores si la decodificación UTF-8 falla
            #print(f"Decodificación fallida con UTF-8, usando latin-1: {decrypted_str}")
            pass

        return decrypted_str
