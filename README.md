This repository is intended to showcase the projects on which I am
currently working. Most of my focus in recent months has been on
developing my coding skills in DRLib (Deep Reinforcement Library). 
because I am fascinated by the power and possibilities of using an
evolutionary model to train artificial neural networks using only random
numbers. I have recently begun developing additional skills in wheelPole
as well.

#### If you just see one thing on here check out this video of it in action.
#### https://youtu.be/l8ELb89swis

I first came across using reinforcement learning when working on the project in
Flappy. I was trying to train neural networks to play a version of
Flappy Bird (an iPhone game), the problem was that there was not a set correct
answer for any one point, more of just a behavior in general that I wanted to
acheive. Using a model of iterating between selection and mutation I found that
I was able to get the exact behavior I wanted only by rewarding it for happenening.

WheelPole uses the same algorithm as Flappy, but uses the code from
DRLib. I am currently using wheelPole for a project in my Electrical Engineering
course. I am building an inverted pendulum controlled by a reaction
wheel. (Example built by someone else:
https://www.youtube.com/watch?v=xlzi8Q5G42k&ab_channel=GraysonG), but
rather than use a PID controller to determine motor output I plan to use
machine learning to control it. WheelPole definitely provides a useful
simulation for this training, although it is still a work in progress and
it is a slightly similified version of reality since
the motors are able to output a constant torque at all times, which is
not quite accurate. Nonetheless, the core of the physics is spot on and
the machine learning seems to be both quick and accurate.

NOTE: I was advised to remove most class projects from my school folder
since it is being posted on a public forum, which could allow other
students to plagiarize my work. I decided to heed this advice, but I
have left one project in the folder from my Data Science Class because
it was for an open-ended prompt.
