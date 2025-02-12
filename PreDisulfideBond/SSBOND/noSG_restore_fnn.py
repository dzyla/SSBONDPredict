# -*- coding:utf-8-*-
import sys
import time
import numpy as np
import tensorflow as tf
import argparse
import os
import math
import warnings
warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
def set_pointdir(basepath):
    checkpoint_dir = os.path.join(basepath,'SSBONDPredict/PreDisulfideBond/static/newmodel')
    return checkpoint_dir
#add energy,only add a parameter result_E into predict
#def predict(args,sess,images,labels,logits,out):
def predict(args,sess,images,labels,logits,out):
    data = args[0]
    id_ord = args[1]
    name = args[2]
    out_ = sess.run(out,feed_dict={images:data.reshape((len(data),100))})
    count = 0
    result_dict = {}
    new_list=[]
    new_list_score = []
    for outi in range(len(out_)):
        # calculating entropy
        if(out_[outi][1] > out_[outi][0]):
            count += 1
            number1 = id_ord[outi][0][4:]
            number2 = id_ord[outi][1][4:]
            distance = abs( int(number1) - int(number2) )
            if distance != 0:
                t = math.log(distance, )
                s = -2.1 - 1.5*8.314*t
                s = '%.4f'% s
            else:
                s = -2.1
                s = '%.4f'% s
            result_dict[id_ord[outi][0]+'-'+id_ord[outi][1]] = str('%.3f'% out_[outi][1]) + ' ' + str(s)
    print ('finish predict.')
    return result_dict


def main(args,basepath):
    sess=tf.compat.v1.Session()
    checkpoint_dir = set_pointdir(basepath)
#    ckpt = tf.train.checkpoint_exists(checkpoint_dir)
    ckpt_path = os.path.join(checkpoint_dir, 'model.ckpt-800')
    #print ckpt_path,'hhhhhhhhhhhhh'
    # modified by xxli)
    saver = tf.compat.v1.train.import_meta_graph(ckpt_path + '.meta')
    saver.restore(sess,ckpt_path)
    graph = tf.compat.v1.get_default_graph()
    images = graph.get_tensor_by_name('image:0')
    labels=graph.get_tensor_by_name('labels:0')
    logits = graph.get_tensor_by_name('softmax_linear/add:0')
    out=tf.nn.softmax(logits=logits)
    result_dict = predict(args,sess,images,labels,logits,out)
    return result_dict

'''''
def main(args,basepath):
    sess=tf.compat.v1.Session()
    checkpoint_dir = set_pointdir(basepath)
#    ckpt = tf.train.checkpoint_exists(checkpoint_dir)
    ckpt_path = os.path.join(checkpoint_dir, 'model.ckpt-800')
    #print ckpt_path,'hhhhhhhhhhhhh'
    # modified by xxli)
    saver = tf.compat.v1.train.import_meta_graph(ckpt_path + '.meta')
    saver.restore(sess,ckpt_path)
    graph = tf.compat.v1.get_default_graph()
    images = graph.get_tensor_by_name('image:0')
    labels=graph.get_tensor_by_name('labels:0')
    logits = graph.get_tensor_by_name('softmax_linear/add:0')
    out=tf.nn.softmax(logits=logits)
    result_dict = predict(args,sess,images,labels,logits,out)
    return result_dict
'''''

if __name__ == '__main__':
    #settings.configure()
    tf.app.run()
