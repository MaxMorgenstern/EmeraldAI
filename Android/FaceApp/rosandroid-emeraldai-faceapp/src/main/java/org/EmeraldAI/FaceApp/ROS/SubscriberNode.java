package org.EmeraldAI.FaceApp.ROS;

import android.util.Log;

import org.EmeraldAI.FaceApp.Eye.EyeAnimation;
import org.ros.message.MessageListener;
import org.ros.namespace.GraphName;
import org.ros.node.AbstractNodeMain;
import org.ros.node.ConnectedNode;
import org.ros.node.NodeMain;
import org.ros.node.topic.Subscriber;

import java.util.Arrays;
import java.util.List;

/**
 * Created by maximilianporzelt on 08.04.17.
 * Note: http://rosjava.github.io/rosjava_core/0.1.6/getting_started.html
 */

public class SubscriberNode extends AbstractNodeMain implements NodeMain {

    private static final String TAG = SubscriberNode.class.getSimpleName();

    @Override
    public GraphName getDefaultNodeName() {
        return GraphName.of("EmeraldFaceApp/SubscriberNode");
    }

    @Override
    public void onStart(ConnectedNode connectedNode) {
        Subscriber<std_msgs.String> subscriber = connectedNode.newSubscriber("/emerald_ai/app/face", std_msgs.String._TYPE);
        subscriber.addMessageListener(new MessageListener<std_msgs.String>() {
            @Override
            public void onNewMessage(std_msgs.String message) {
                Log.i(TAG, "I heard: \"" + message.getData() + "\"");
                List<String> messageData = Arrays.asList(message.getData().split("\\|"));

                if (messageData.size() == 2) {
                    EyeAnimation ea = new EyeAnimation();
                    ea.TriggerAnimation(messageData.get(1));
                }
            }
        });
    }
}
