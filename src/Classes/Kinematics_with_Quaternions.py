#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
In this class different kinematic and dynamic equalities are calculated

"""

# TODO: do the orientation calculations by KF later by yourself using gyro and acc measurements. Now use the orientation data that Xsens provides
# TODO: in q_invert(), check if the input is a unit quaternion

# imports
# import Data.data_logger_module as data_logger
import logging
import rospy
import numpy as np
from math import pi as pi
from math import sqrt
import pyquaternion as pq
from sensor_msgs.msg import JointState
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_matrix as q2m
from tf.transformations import euler_from_matrix as m2e
from tf.transformations import euler_from_quaternion as q2e
from tf.transformations import quaternion_from_matrix as m2q
from tf.transformations import rotation_matrix
from tf.transformations import quaternion_about_axis
from tf.transformations import quaternion_multiply
from tf.transformations import quaternion_conjugate as conj
import scipy.integrate as integrate


# Private Globals
_g = np.array([0, -9.81, 0])  # gravity vector in global frame


# Private Functions
def q_rotate(q, v):
    ''''
    Computes v_rotated = qvq* fastly
    @params q: rotating quaternion represented as numpy array [q0, q1, q2, q3] -> [w, x, y, z]
    @params v: to be rotated vector. Represented as numpy array. Expressed as pure quaternion. [v0, v1, v2] -> [x, y, z]
    '''
    v_rotated = np.array([v[0]*(q[0]**2 + q[1]**2 - q[2]**2 - q[3]**2) + 2*v[1]*(q[1]*q[2]-q[0]*q[3]) + 2*v[2]*(q[0]*q[2] + q[1]*q[3]),
                          2*v[0]*(q[0]*q[3] + q[1]*q[2]) + v[1]*(q[0]**2 - q[1]**2 + q[2]**2 - q[3]**2) + 2*v[2]*(q[2]*q[3] - q[0]*q[1]),
                          2*v[0]*(q[1]*q[3] - q[0]*q[2]) + 2*v[1]*(q[0]*q[1] + q[2]*q[3]) + v[2]*(q[0]**2 - q[1]**2 - q[2]**2 + q[3]**2)])

    # v2 = np.concatenate([[0], v1], axis=0)
    # q2 = quaternion_multiply(v2, conj(q1))
    # q2 = quaternion_multiply(q1, q2)
    return v_rotated


def q_invert(q):
    '''
    Invert unit quaternion
    '''
    # print "q input:{0}".format(q)
    q_test = pq.Quaternion()
    q_inverted = Quaternion()
    if type(q) == Quaternion:
        # if the dtype is tf.quaternion
        q_inverted.x = -q.x
        q_inverted.y = -q.y
        q_inverted.z = -q.z
        q_inverted.w = q.w
        return q_inverted
    elif type(q) == np.ndarray:
        q_inverted = [q[0], -q[1], -q[2], -q[3]]
        return q_inverted
    elif type(q) == type(q_test):
        q_inverted = pq.Quaternion(q.w, -q.x, -q.y, -q.z)
        # print "q inverted:{0}".format(q_inverted)
        return q_inverted
    else:
        print "unknown dtype"
        return q


def q_multiply(q, p):
    '''
    Multiply quaternions
    '''
    q_test = pq.Quaternion()
    if type(q) == Quaternion:
        q_multiplied = Quaternion()
        q_multiplied.w = q.w*p.w - q.x*p.x - q.y*p.y - q.z*p.z
        q_multiplied.x = q.w*p.x + q.x*p.w + q.y*p.z - q.z*p.y
        q_multiplied.y = q.w*p.y + q.y*p.w - q.x*p.z + q.z*p.x
        q_multiplied.z = q.w*p.z + q.z*p.w + q.x*p.y - q.y*p.x
        return q_multiplied
    elif type(q) == np.ndarray:
        q_multiplied = np.array([0.0, 0.0, 0.0, 1.0])  # 'xyzw'
        q_multiplied[0] = q[3]*p[0] + q[0]*p[3] + q[1]*p[2] - q[2]*p[1]
        q_multiplied[1] = q[3]*p[1] + q[1]*p[3] - q[0]*p[2] + q[2]*p[0]
        q_multiplied[2] = q[3]*p[2] + q[2]*p[3] + q[0]*p[1] - q[1]*p[0]
        q_multiplied[3] = q[3]*p[3] - q[0]*p[0] - q[1]*p[1] - q[2]*p[2]
        return q_multiplied
    elif type(q) == type(q_test):
        q_multiplied = q*p
        return q_multiplied
    else:
        print "unknown dtype"
        return q


def q_tf_convert(q):
    '''
    Convert geometry_msgs.Quaternion objects into numpy array for making use of in tf.transformations
    '''
    q_converted = np.array([0.0, 0.0, 0.0, 1.0])
    q_converted[0] = q.x
    q_converted[1] = q.y
    q_converted[2] = q.z
    q_converted[3] = q.w
    return q_converted


def q_magnitude(q):
    q_mag = sqrt((q.w**2 + q.x**2 + q.y**2 + q.z**2))
    return q_mag






# body segment lengths
pivot_to_shoulder = np.array([15, 0, 0])
shoulder_to_elbow = np.array([0, -25, 0])
elbow_to_wrist = np.array([0, -22, 0])

# sensor placements
s_shoulder = shoulder_to_elbow + np.array([4, 0, 0])
s_elbow = elbow_to_wrist + np.array([3, 0, 0])
s_wrist = np.array([2, -5, 0])


# Functions
def body_in_global(q_sensor_to_global, q_sensor_to_body):
    '''
    Known orientation of each segment and given sensor orientation in global frame, calculates the body orientation in global frame.
    {GB}q = {GS}q * {BS}q'  (q' is the conjugate quaternion)
    @param q_sensor_to_global: Calculated orientation in quaternion from sensor to global frame (given by xsens for now)
    @param q_sensor_to_body: Known measurement of sensor placement wrt body origin
    @ returns: Orientation from body frame to global frame in quaternion
    '''
    q_body_to_global = quaternion_multiply(q_sensor_to_global, conj(q_sensor_to_body))
    return q_body_to_global


def angular_vel_to_orientation(q_sensor, ang_vel):
    '''
    Calculates the rotation from sensor frame to global frame by integration:
    {GS}q_t_dot = 0.5 * {GS}q_t * omega_t
    omega_t = (0, w_x, w_y, w_z) : angular velocity w_t
    @param q_sensor: {GS}q_t: Calculated orientation
    @param ang_vel: Gyroscope reading
    @returns: Orientation from sensor frame to global frame
    '''
    pass


def acc_to_pos(q_sensor, acc_sensor, dt):
    '''
    Calculates integrated position from accelerometer readings
    {G}a_t - {G}g = {GS}q_t * ({S}a_t - {S}g) * {GS}q'_t
    {g}p_t_dotdot = {G}a_t
    @param
    '''
    acc_total = quaternion_multiply(q_sensor, quaternion_multiply(acc_sensor, conj(q_sensor)))
    p_hat_acc_cur = integrate.simps(integrate.simps(acc_total - _g, dx=dt))  # 3x1
    return p_hat_acc_cur


def segment_kinematics(p_u_prev, q_u, s_u, q_u_conj):
    '''
    Calculates the origin of the next body segment in global frame.
    {G}p_u_next = {G}p_u_prev + {GB}q_u * {B}s_u * {GB}q_u_conj
    @param p_u_prev: position of the previous joint in global frame
    @param q_u: orientation of the respective body part from body to global frame
    @param s_u: the length of the respective body part
    @returns: the next body segment's origin position.

    '''
    pass


def join_update():
    '''
    Calculates the joint position using KF.

    TODO: every C matrix should be different than each other. for shoulder for example and for knee.
    '''
    C = np.concatenate((np.eye(3), -np.eye(3)), axis=1)

    pass
