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

package org.EmeraldAI.FaceApp.ROS;

import android.util.Log;

import org.ros.concurrent.CancellableLoop;
import org.ros.namespace.GraphName;
import org.ros.node.AbstractNodeMain;
import org.ros.node.ConnectedNode;
import org.ros.node.NodeMain;
import org.ros.node.topic.Publisher;

import java.text.SimpleDateFormat;
import java.util.Date;

public class PublisherNode extends AbstractNodeMain implements NodeMain {

    private static final String TAG = PublisherNode.class.getSimpleName();

    @Override
    public GraphName getDefaultNodeName() {
        return GraphName.of("EmeraldFaceApp/PublisherNode");
    }

    private Publisher<std_msgs.String> brainPublisher;

    @Override
    public void onStart(ConnectedNode connectedNode) {
        brainPublisher = connectedNode.newPublisher(GraphName.of("to_brain"), std_msgs.String._TYPE);

        final Publisher<std_msgs.String> pingPublisher = connectedNode.newPublisher(GraphName.of("Ping"), std_msgs.String._TYPE);

        final CancellableLoop loop = new CancellableLoop() {
            @Override
            protected void loop() throws InterruptedException {
                // retrieve current system time
                String time = new SimpleDateFormat("HH:mm:ss").format(new Date());

                Log.i(TAG, "Sending to 'ping': \"FaceApp|" + time + "\"");

                // create and publish a simple string message
                std_msgs.String str = pingPublisher.newMessage();
                str.setData("FaceApp|" + time);
                pingPublisher.publish(str);

                // go to sleep for 10 seconds
                Thread.sleep(10000);
            }
        };
        connectedNode.executeCancellableLoop(loop);
    }

    public void ToBrain(String data)
    {
        Log.i(TAG, "Sending to 'to_brain': \"FaceApp|" + data + "\"");

        std_msgs.String str = brainPublisher.newMessage();
        str.setData("FaceApp|" + data);
        brainPublisher.publish(str);
    }

}
