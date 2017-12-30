#!/usr/bin/python
# -*- coding: utf-8 -*-

class PIDController():

    def __init__(self, timeNow):
        ### initialize variables
        self.target = 0
        self.motor = 0
        self.vel = 0
        self.integral = 0
        self.error = 0
        self.derivative = 0
        self.previousError = 0
        self.wheelPrev = 0
        self.wheelLatest = 0
        self.then = 0
        self.wheelMult = 0
        self.prevEncoder = 0


        # TODO !!!!!!!!!!!!!!!!

        ### get parameters ####
        self.Kp = 10#rospy.get_param('~Kp',10)
        self.Ki = 10#rospy.get_param('~Ki',10)
        self.Kd = 0.001#rospy.get_param('~Kd',0.001)
        self.outMin = -255#rospy.get_param('~out_min',-255)
        self.outMax = 255#rospy.get_param('~out_max',255)
        self.rollingPts = 2#rospy.get_param('~rolling_pts',2)
        self.timeoutTicks = 4#rospy.get_param('~timeout_ticks',4)
        self.ticksPerMeter = 20#rospy.get_param('ticks_meter', 20)
        self.velThreshold = 0.001#rospy.get_param('~vel_threshold', 0.001)
        self.encoderMin = -32768#rospy.get_param('encoder_min', -32768)
        self.encoderMax = 32768#rospy.get_param('encoder_max', 32768)
        self.encoderLowWrap = (self.encoderMax - self.encoderMin) * 0.3 + self.encoderMin#rospy.get_param('wheel_low_wrap', (self.encoderMax - self.encoderMin) * 0.3 + self.encoderMin )
        self.encoderHighWrap = (self.encoderMax - self.encoderMin) * 0.7 + self.encoderMin#rospy.get_param('wheel_high_wrap', (self.encoderMax - self.encoderMin) * 0.7 + self.encoderMin )
        self.prevVel = [0.0] * self.rollingPts
        self.wheelLatest = 0.0
        self.prevPidTime = timeNow
        self.ticksSinceLastTarget = self.timeoutTicks


    def SetWheel(self, data):
        if (data < self.encoderLowWrap and self.prevEncoder > self.encoderHighWrap) :
            self.wheelMult = self.wheelMult + 1

        if (data > self.encoderHighWrap and self.prevEncoder < self.encoderLowWrap) :
            self.wheelMult = self.wheelMult - 1

        self.wheelLatest = 1.0 * (data + self.wheelMult * (self.encoderMax - self.encoderMin)) / self.ticksPerMeter
        self.prevEncoder = data


    def SetTarget(self, data):
        self.target = data
        self.ticksSinceLastTarget = 0


    def MainLoop(self, timeNow):
        self.RospyTimeNow = timeNow
        self.previousError = 0.0
        self.prevVel = [0.0] * self.rollingPts
        self.integral = 0.0
        self.error = 0.0
        self.derivative = 0.0
        self.vel = 0.0

        # only do the loop if we've recently recieved a target velocity message
        if self.ticksSinceLastTarget < self.timeoutTicks:
            self.__calcVelocity()
            self.__doPid()
            self.ticksSinceLastTarget += 1

            return self.motor

        return 0


    def __calcVelocity(self):
        self.dt_duration = self.RospyTimeNow - self.then
        self.dt = self.dt_duration.to_sec()

        if (self.wheelLatest == self.wheelPrev):
            # we haven't received an updated wheel lately
            cur_vel = (1 / self.ticksPerMeter) / self.dt    # if we got a tick right now, this would be the velocity
            if abs(cur_vel) < self.velThreshold:
                # if the velocity is < threshold, consider our velocity 0
                self.__appendVel(0)
                self.__calcRollingVel()
            else:
                if abs(cur_vel) < self.vel:
                    # we know we're slower than what we're currently publishing as a velocity
                    self.__appendVel(cur_vel)
                    self.__calcRollingVel()

        else:
            # we received a new wheel value
            cur_vel = (self.wheelLatest - self.wheelPrev) / self.dt
            self.__appendVel(cur_vel)
            self.__calcRollingVel()
            self.wheelPrev = self.wheelLatest
            self.then = self.RospyTimeNow

        return self.vel


    def __appendVel(self, val):
        self.prevVel.append(val)
        del self.prevVel[0]


    def __calcRollingVel(self):
        p = array(self.prevVel)
        self.vel = p.mean()

    def __doPid(self):
        pidDtDuration = self.RospyTimeNow - self.prevPidTime
        pidDt = pidDtDuration.to_sec()
        self.prevPidTime = self.RospyTimeNow

        self.error = self.target - self.vel
        self.integral = self.integral + (self.error * pidDt)
        self.derivative = (self.error - self.previousError) / pidDt
        self.previousError = self.error

        self.motor = (self.Kp * self.error) + (self.Ki * self.integral) + (self.Kd * self.derivative)

        if self.motor > self.outMax:
            self.motor = self.outMax
            self.integral = self.integral - (self.error * pidDt)
        if self.motor < self.outMin:
            self.motor = self.outMin
            self.integral = self.integral - (self.error * pidDt)

        if (self.target == 0):
            self.motor = 0

