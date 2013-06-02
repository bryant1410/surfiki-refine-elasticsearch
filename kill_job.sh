#!/bin/bash

kill -9 `ps -aef | grep $1 | grep -v grep | awk '{print $2}'`
