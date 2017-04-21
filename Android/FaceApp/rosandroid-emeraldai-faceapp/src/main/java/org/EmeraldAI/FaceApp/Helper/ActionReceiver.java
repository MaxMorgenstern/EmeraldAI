package org.EmeraldAI.FaceApp.Helper;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

import static android.content.ContentValues.TAG;

/**
 * Created by mporzelt on 21.04.2017.
 */

public class ActionReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent.getAction().equals(Intent.ACTION_SCREEN_ON)) {
            Log.e(TAG, "Screen turned on");
            // TODO - Notify ROS Master
        }
        if (intent.getAction().equals(Intent.ACTION_SCREEN_OFF)) {
            Log.e(TAG, "Screen turned off");
            // TODO - Notify ROS Master
        }
    }
}
