/*
 * Copyright (C) 2014 Oliver Degener.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */

package org.EmeraldAI.FaceApp;

import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;

import org.EmeraldAI.FaceApp.CustomViews.GifImageView;
import org.EmeraldAI.FaceApp.ROS.SimplePublisherNode;
import org.EmeraldAI.FaceApp.ROS.SimpleSubscriberNode;
import org.ros.address.InetAddressFactory;
import org.ros.android.RosActivity;
import org.ros.node.NodeConfiguration;
import org.ros.node.NodeMain;
import org.ros.node.NodeMainExecutor;

import java.io.IOException;
import java.io.InputStream;

public class MainActivity extends RosActivity {

    public MainActivity() {
        super("RosAndroidExample", "RosAndroidExample");
    }

    //Random rand = new Random();
    Handler handler = new Handler();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // landscape mode
        super.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);

        // keep screen on
        //getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);


        Runnable r = new Runnable() {
            public void run() {
                // TODO: check EyeState Queue
                handler.postDelayed(this, 100);
            }
        };
        handler.postDelayed(r, 100);

        // load image and play
        GifImageView gifImageView = (GifImageView) findViewById(R.id.GifImageView);
        try {
            InputStream ins = getAssets().open("blinkv2.gif");
            gifImageView.SetGifImageStream(ins, true, 5000);
        }
        catch(IOException ex) {
            return;
        }
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        View decorView = getWindow().getDecorView();
        if (hasFocus) {
            decorView.setSystemUiVisibility(
                    View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                            | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                            | View.SYSTEM_UI_FLAG_FULLSCREEN
                            | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
        }
    }

    @Override
    protected void init(NodeMainExecutor nodeMainExecutor) {
        NodeConfiguration nodeConfiguration = NodeConfiguration.newPublic(InetAddressFactory.newNonLoopback().getHostAddress());
        nodeConfiguration.setMasterUri(getMasterUri());

        NodeMain node = new SimplePublisherNode();
        nodeMainExecutor.execute(node, nodeConfiguration);

        NodeMain node2 = new SimpleSubscriberNode();
        nodeMainExecutor.execute(node2, nodeConfiguration);
    }
}
