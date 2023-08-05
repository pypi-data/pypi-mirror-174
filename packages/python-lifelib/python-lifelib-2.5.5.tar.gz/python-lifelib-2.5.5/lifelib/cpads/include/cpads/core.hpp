#pragma once

#include <stdint.h>
#include <stddef.h>
#include <iostream>
#include <utility>
#include <type_traits>
#include <cmath>

// an inlined host function:
#define _HI_ __attribute__((always_inline)) inline

// an inlined device function:
#define _DI_ __attribute__((always_inline)) __device__ inline

// an inlined host/device function:
#ifdef __CUDACC__
#define _HD_ __attribute__((always_inline)) __host__ __device__ inline
#else
#define _HD_ _HI_
#endif

// an inlined constexpr host/device function:
#define _HDC_ _HD_ constexpr

// static assert, but in green:
#define colour_assert(x, y) static_assert(x, "\033[32;1m" y "\033[0m")

// useful for defining classes by composition instead of inheritance:
#define INHERIT_COMPARATORS_FROM(ThisType, member, decorator) \
    decorator bool operator==(const ThisType& rhs) const { return member == rhs . member; } \
    decorator bool operator!=(const ThisType& rhs) const { return member != rhs . member; } \
    decorator bool operator<=(const ThisType& rhs) const { return member <= rhs . member; } \
    decorator bool operator>=(const ThisType& rhs) const { return member >= rhs . member; } \
    decorator bool operator< (const ThisType& rhs) const { return member <  rhs . member; } \
    decorator bool operator> (const ThisType& rhs) const { return member >  rhs . member; }

#define INHERIT_ACCESSORS_FROM(ElementType, member, decorator) \
    decorator ElementType& operator[](size_t i) { return member[i]; } \
    decorator const ElementType& operator[](size_t i) const { return member[i]; } 

namespace hh {

template<typename T>
_HDC_ T min(const T &a, const T &b) {
    return (a < b) ? a : b;
}

template<typename T>
_HDC_ T max(const T &a, const T &b) {
    return (a < b) ? b : a;
}

typedef __uint128_t u128;
typedef __int128_t i128;

/**
 * In-place multiplication of 64-bit operands to yield 128-bit result.
 */
_HD_ void mul64x64(uint64_t &low, uint64_t &high) {
    #ifdef __CUDA_ARCH__
    auto product = low * high;
    high = __umul64hi(low, high);
    low = product;
    #else
    u128 product = ((u128) low) * high;
    high = (uint64_t) (product >> 64);
    low = (uint64_t) product;
    #endif
}

_HDC_ uint64_t fibmix_perm_1(uint64_t input) {
    return input * (11400714819323198485ull + (input << 1));
}

_HDC_ uint64_t fibmix_perm_2(uint64_t a) {
    return a ^ (a >> ((a >> 59) + 5));
}

_HDC_ uint64_t fibmix(uint64_t input) {
    return fibmix_perm_2(fibmix_perm_1(input));
}

colour_assert(fibmix(0) == 0, "fibmix must be a zero-preserving permutation");

_HD_ int popc32(uint32_t x) {
    #ifdef __CUDA_ARCH__
    return __popc(x);
    #else
    return __builtin_popcount(x);
    #endif
}

_HD_ int popc64(uint64_t x) {
    #ifdef __CUDA_ARCH__
    return __popcll(x);
    #else
    return __builtin_popcountll(x);
    #endif
}

_HD_ int ffs32(uint32_t x) {
    #ifdef __CUDA_ARCH__
    return __ffs(x);
    #else
    return __builtin_ffs(x);
    #endif
}

_HD_ int ffs64(uint64_t x) {
    #ifdef __CUDA_ARCH__
    return __ffsll(x);
    #else
    return __builtin_ffsll(x);
    #endif
}

_HD_ int clz32(uint32_t x) {
    #ifdef __CUDA_ARCH__
    return __clz(x);
    #else
    return __builtin_clz(x);
    #endif
}

_HD_ int clz64(uint64_t x) {
    #ifdef __CUDA_ARCH__
    return __clzll(x);
    #else
    return __builtin_clzll(x);
    #endif
}

_HD_ int ctz32(uint32_t x) {
    #ifdef __CUDA_ARCH__
    return __ffs(x) - 1;
    #else
    return __builtin_ctz(x);
    #endif
}

_HD_ int ctz64(uint64_t x) {
    #ifdef __CUDA_ARCH__
    return __ffsll(x) - 1;
    #else
    return __builtin_ctzll(x);
    #endif
}

/**
 * Computes the integer part of the square-root of the input.
 * This is valid for all 64-bit unsigned integers.
 */
_HD_ uint64_t floor_sqrt(uint64_t x) {
    uint64_t y = ((uint64_t) (std::sqrt((double) x) - 0.5));
    if (2*y < x - y*y) { y++; }
    return y;
}

} // namespace hh
