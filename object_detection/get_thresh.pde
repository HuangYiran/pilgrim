/*
In order to remove the affect of the situation, we only detect the people in limitted region(between minThresh and maxThres).
This program is used to get the suitable value of minThresh and maxThresh.
Press i to save the thresh in /tmp/thresh
*/


import org.openkinect.processing.*;
import java.io.*;
import java.lang.reflect.*;

Kinect kinect;

int skip = 1;
PImage img;

void setup() {
  size(512, 484);
  kinect = new Kinect(this);
  kinect.initDepth();
  kinect.initVideo();
  //kinect.enableIR(ir);
  //kinect.enableColorDepth(colorDepth);
  img = createImage(kinect.width, kinect.height, RGB);
}


void draw() {
  background(0);
  //img.loadPixels();
  float minThresh = map(mouseX, 0, width, 0, 2048);
  float maxThresh = map(mouseY, 0, height, 0, 2048);
  //int minThresh = 0;
  //int maxThresh = 1000;
  int[] depth = kinect.getRawDepth();
  
  for(int x = 0; x < kinect.width; x += skip){
    for(int y = 0; y < kinect.height; y += skip){
      int offset = x + y * kinect.width;
      int d = depth[offset];
      if(d > minThresh && d < maxThresh){
        img.pixels[offset] = color(255, 0, 150);
      }else{
        img.pixels[offset] = color(22,22,22);
      }
    }
  }
  img.updatePixels();
  //image(kinect.getVideoImage(), 0, 0);
  image(img, 0, 0);
  fill(255);
  textSize(32);
  text(minThresh + " " + maxThresh, 10, 64);
}

void keyPressed() {
  if (key == 'i'){
    try{
      float minThresh = map(mouseX, 0, width, 0, 4500);
      float maxThresh = map(mouseY, 0, height, 0, 4500);
      FileWriter fw = new FileWriter("/tmp/thresh");
      fw.write(minThresh + " " + maxThresh);
      fw.close();
    } catch (IOException e) {
      e.printStackTrace();
    } 
  }
}
