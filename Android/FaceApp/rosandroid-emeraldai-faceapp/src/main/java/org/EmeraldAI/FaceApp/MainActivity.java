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

import android.content.BroadcastReceiver;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.os.Handler;
import android.os.SystemClock;
import android.util.Log;
import android.view.View;

import org.EmeraldAI.FaceApp.CustomViews.GifImageView;
import org.EmeraldAI.FaceApp.Eye.EyeAnimation;
import org.EmeraldAI.FaceApp.Eye.EyeAnimationObject;
import org.EmeraldAI.FaceApp.Eye.EyeState;
import org.EmeraldAI.FaceApp.Helper.ActionReceiver;
import org.EmeraldAI.FaceApp.ROS.PublisherNode;
import org.EmeraldAI.FaceApp.ROS.SubscriberNode;
import org.ros.address.InetAddressFactory;
import org.ros.android.RosActivity;
import org.ros.node.NodeConfiguration;
import org.ros.node.NodeMain;
import org.ros.node.NodeMainExecutor;

import java.io.IOException;
import java.io.InputStream;

import static android.content.ContentValues.TAG;

public class MainActivity extends RosActivity {

    public MainActivity() {
        super("RosAndroidExample", "RosAndroidExample");
    }

    Handler handler = new Handler();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // TODO: remove
        // landscape mode
        // super.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);

        // keep screen on
        // getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);


        Runnable r = new Runnable() {
            public void run() {
                EyeState es = EyeState.getInstance();
                EyeAnimation ea = new EyeAnimation();

                ea.BlinkUpdater();
                ea.IdleUpdater();

                Log.i(TAG, "Main - Idle: " + es.IdleMode + " - QueueSize: " + es.GetQueueSize() + " - Timestamp: " + es.AnimationEndTimestamp);

                long now = SystemClock.uptimeMillis();
                long waitUntil = (es.CurrentAnimation != null) ?
                        (es.AnimationEndTimestamp + es.CurrentAnimation.MinDelayAfterAnimation) : 0;

                if(waitUntil <= now && !es.AnimationRunning && es.GetQueueSize() > 0)
                {
                    EyeAnimationObject eao = es.GetFromQueue();
                    GifImageView gifImageView = (GifImageView) findViewById(R.id.GifImageView);
                    try
                    {
                        InputStream ins = getAssets().open(eao.AnimationObject + ".gif");
                        gifImageView.SetGifImageStream(ins, false);
                    } catch (IOException ex) {
                        Log.e(TAG, "Error on calling new image " + ex.toString());
                    }
                }

                handler.postDelayed(this, 100);
            }
        };
        handler.postDelayed(r, 100);

        Log.i(TAG, "add blink from main");
        new EyeAnimation().TriggerAnimation("blink");
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

        NodeMain node = new PublisherNode();
        nodeMainExecutor.execute(node, nodeConfiguration);

        NodeMain node2 = new SubscriberNode();
        nodeMainExecutor.execute(node2, nodeConfiguration);

        IntentFilter filter = new IntentFilter();
        filter.addAction(Intent.ACTION_SCREEN_OFF);
        filter.addAction(Intent.ACTION_SCREEN_ON);
        BroadcastReceiver mReceiver = new ActionReceiver();
        registerReceiver(mReceiver, filter);
    }
}
