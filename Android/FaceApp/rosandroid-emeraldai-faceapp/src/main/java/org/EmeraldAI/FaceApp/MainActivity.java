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

import android.os.Bundle;

import org.ros.address.InetAddressFactory;
import org.ros.android.RosActivity;
import org.ros.node.NodeConfiguration;
import org.ros.node.NodeMain;
import org.ros.node.NodeMainExecutor;
import org.EmeraldAI.FaceApp.GifImageView;

import java.io.IOException;
import java.io.InputStream;

public class MainActivity extends RosActivity {

    public MainActivity() {
        super("RosAndroidExample", "RosAndroidExample");
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // maybe try: https://github.com/koral--/android-gif-drawable

        // load image and play
        GifImageView gifImageView = (GifImageView) findViewById(R.id.GifImageView);
        try {
            InputStream ins = getAssets().open("blinkv2.gif");
            gifImageView.setGifImageStream(ins);
        }
        catch(IOException ex) {
            return;
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
