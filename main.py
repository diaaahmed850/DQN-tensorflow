from __future__ import print_function
import random
import tensorflow as tf

from dqn.agent import Agent
from dqn.environment import GymEnvironment, SimpleGymEnvironment
from config import get_config
import argparse
flags = tf.app.flags
parser = argparse.ArgumentParser()
parser.add_argument('--model',type=str,default='m1',help='Type of model')
parser.add_argument('--dueling',type=bool,default=False,help='Whether to use dueling deep q-network')
parser.add_argument('--double_q',type=bool,default=False,help='Whether to use double q-learning')

parser.add_argument('--env_name',type=str,default='Breakout-v0',help='The name of gym environment to use')
parser.add_argument('--action_repeat',type=int,default=4,help='The number of action to be repeated')

parser.add_argument('--use_gpu',type=bool,default=True,help='Whether to use gpu or not')
parser.add_argument('--gpu_fraction',type=str,default='7/10',help='idx / # of gpu fraction e.g. 1/3, 2/3, 3/3')
parser.add_argument('--is_train',type=bool,default=False,help='Whether to do training or testing')
parser.add_argument('--display',type=bool,default=True,help='Whether to do display the game screen or not')
parser.add_argument('--random_seed',type=int,default=123,help='Value of random seed')



"""
# Model
flags.DEFINE_string('model', 'm1', 'Type of model')
flags.DEFINE_boolean('dueling', False, 'Whether to use dueling deep q-network')
flags.DEFINE_boolean('double_q', False, 'Whether to use double q-learning')

# Environment
flags.DEFINE_string('env_name', 'Breakout-v0', 'The name of gym environment to use')
flags.DEFINE_integer('action_repeat', 4, 'The number of action to be repeated')

# Etc
flags.DEFINE_boolean('use_gpu', True, 'Whether to use gpu or not')
flags.DEFINE_string('gpu_fraction', '1/1', 'idx / # of gpu fraction e.g. 1/3, 2/3, 3/3')
flags.DEFINE_boolean('display', False, 'Whether to do display the game screen or not')
flags.DEFINE_boolean('is_train', True, 'Whether to do training or testing')
flags.DEFINE_integer('random_seed', 123, 'Value of random seed')

FLAGS = flags.FLAGS
"""
FLAGS = parser.parse_args()
print(FLAGS.is_train)
# Set random seed
tf.set_random_seed(FLAGS.random_seed)
random.seed(FLAGS.random_seed)

if FLAGS.gpu_fraction == '':
  raise ValueError("--gpu_fraction should be defined")

def calc_gpu_fraction(fraction_string):
  idx, num = fraction_string.split('/')
  idx, num = float(idx), float(num)

  fraction = 1 / (num - idx + 1)
  print(" [*] GPU : %.4f" % fraction)
  return fraction

def main(_):
  gpu_options = tf.GPUOptions(
      per_process_gpu_memory_fraction=calc_gpu_fraction(FLAGS.gpu_fraction))

  with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
    config = get_config(FLAGS) or FLAGS

    if config.env_type == 'simple':
      env = SimpleGymEnvironment(config)
    else:
      env = GymEnvironment(config)

    if not tf.test.is_gpu_available() and True:
      raise Exception("use_gpu flag is true when no GPUs are available")

    if not True:
      config.cnn_format = 'NHWC'

    agent = Agent(config, env, sess)

    if FLAGS.is_train:
      agent.train()
       
    else:
      agent.play()
       

if __name__ == '__main__':
  tf.app.run()
