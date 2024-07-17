#ifdef TEST_SUBBYTES

__constant__ char sbox[256];

#endif

#ifndef LUT_IN_SHARED
__device__ void SubBytes(char* block){
#else
__device__ void SubBytes(char* block, char* sbox){
#endif
    for(unsigned int i = 0; i < 16; i++){
        block[i] = sbox[(unsigned char) block[i]];
    }
}

#ifdef TEST_SUBBYTES

__global__ void SubByteTest(char* message, const unsigned int length){
    int idx = (threadIdx.x + blockDim.x * blockIdx.x) * 16;
    if (idx + 16 <= length){
        SubBytes(message + idx);
    }
}

#endif
