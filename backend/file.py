import os
import pandas as pd
import tensorflow as tf
import flask
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import numpy as np
import time

print(tf.__version__)