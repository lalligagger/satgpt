#!/usr/bin/env python
# encoding: utf-8

def print_something(something="module test"):
    print(something, flush=True)
    return something

if __name__ == '__main__':
    print_something()