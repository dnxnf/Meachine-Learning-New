#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：19NumpyJudge.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午9:42
从一个 N * M（N ≤ M）的矩阵中选出 N 个数，任意两个数字不能在同一行或同一列，
求选出来的 N 个数中第 K 大的数字的最小值是多少。
输入描述
输入矩阵要求：1 ≤ K ≤ N ≤ M ≤ 150
输入格式：
N M K
N*M矩阵
输出描述
N*M 的矩阵中可以选出 M! / N! 种组合数组，每个组合数组种第 K 大的数中的最小值。无需考虑重复数字，直接取字典排序结果即可。
备注
注意：结果是第 K 大的数字的最小值
eg:
3 4 2
1 5 6 6
8 3 4 3
6 8 6 3
out:3
'''

