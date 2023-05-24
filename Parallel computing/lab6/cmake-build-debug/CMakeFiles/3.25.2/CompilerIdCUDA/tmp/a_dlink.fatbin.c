#ifndef __SKIP_INTERNAL_FATBINARY_HEADERS
#include "fatbinary_section.h"
#endif
#define __CUDAFATBINSECTION  ".nvFatBinSegment"
#define __CUDAFATBINDATASECTION  ".nv_fatbin"
#ifdef __cplusplus
extern "C" {
#endif

#pragma const_seg(__CUDAFATBINDATASECTION)
static const __declspec(allocate(__CUDAFATBINDATASECTION)) unsigned long long fatbinData[]= {0x00100001ba55ed50ull,0x0000000000000338ull,0x0000004001010002ull,0x00000000000002f8ull,
0x0000000000000000ull,0x0000003400010007ull,0x0000000000000000ull,0x0000000000000041ull,
0x0000000000000000ull,0x0000000000000000ull,0x33010102464c457full,0x0000000000000007ull,
0x0000007900be0002ull,0x0000000000000000ull,0x0000000000000288ull,0x0000000000000148ull,
0x0038004000340534ull,0x0001000500400002ull,0x7472747368732e00ull,0x747274732e006261ull,
0x746d79732e006261ull,0x746d79732e006261ull,0x78646e68735f6261ull,0x7466752e766e2e00ull,
0x2e007972746e652eull,0x006f666e692e766eull,0x6c6c61632e766e2eull,0x6e2e006870617267ull,
0x746f746f72702e76ull,0x68732e0000657079ull,0x2e00626174727473ull,0x2e00626174727473ull,
0x2e006261746d7973ull,0x735f6261746d7973ull,0x766e2e0078646e68ull,0x746e652e7466752eull,
0x692e766e2e007972ull,0x2e766e2e006f666eull,0x706172676c6c6163ull,0x72702e766e2e0068ull,
0x00657079746f746full,0x0000000000000000ull,0x0000000000000000ull,0x0000000000000000ull,
0x0004000300000040ull,0x0000000000000000ull,0x0000000000000000ull,0xffffffff00000000ull,
0xfffffffe00000000ull,0xfffffffd00000000ull,0xfffffffc00000000ull,0x0000000000000000ull,
0x0000000000000000ull,0x0000000000000000ull,0x0000000000000000ull,0x0000000000000000ull,
0x0000000000000000ull,0x0000000000000000ull,0x0000000000000000ull,0x0000000300000001ull,
0x0000000000000000ull,0x0000000000000000ull,0x0000000000000040ull,0x000000000000005cull,
0x0000000000000000ull,0x0000000000000001ull,0x0000000000000000ull,0x000000030000000bull,
0x0000000000000000ull,0x0000000000000000ull,0x000000000000009cull,0x000000000000005cull,
0x0000000000000000ull,0x0000000000000001ull,0x0000000000000000ull,0x0000000200000013ull,
0x0000000000000000ull,0x0000000000000000ull,0x00000000000000f8ull,0x0000000000000030ull,
0x0000000200000002ull,0x0000000000000008ull,0x0000000000000018ull,0x7000000100000040ull,
0x0000000000000000ull,0x0000000000000000ull,0x0000000000000128ull,0x0000000000000020ull,
0x0000000000000005ull,0x0000000000000004ull,0x0000000000000008ull,0x0000000500000006ull,
0x0000000000000288ull,0x0000000000000000ull,0x0000000000000000ull,0x0000000000000070ull,
0x0000000000000070ull,0x0000000000000008ull,0x0000000500000001ull,0x0000000000000288ull,
0x0000000000000000ull,0x0000000000000000ull,0x0000000000000070ull,0x0000000000000070ull,
0x0000000000000008ull
};
#pragma const_seg()

#ifdef __cplusplus
}
#endif

#ifdef __cplusplus
extern "C" {
#endif
#pragma const_seg(".nvFatBinSegment")
__declspec(allocate(__CUDAFATBINSECTION)) __declspec(align(8)) static const __fatBinC_Wrapper_t __fatDeviceText= 
	{ 0x466243b1, 2, fatbinData, (void**)__cudaPrelinkedFatbins };
#pragma const_seg()
#ifdef __cplusplus
}
#endif
