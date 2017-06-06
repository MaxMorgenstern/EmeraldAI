package org.EmeraldAI.FaceApp.Eye;

import android.os.SystemClock;
import android.util.Log;

import java.util.LinkedList;
import java.util.Queue;

import static android.content.ContentValues.TAG;

/**
 * Created by maximilianporzelt on 15.04.17.
 */

public class EyeState {
    private static final EyeState ourInstance = new EyeState();

    public static EyeState getInstance() {
        return ourInstance;
    }

    public boolean AnimationRunning;
    public boolean Loop;
    public long AnimationEndTimestamp;

    public boolean IdleMode;
    public long IdleDelay;

    public EyeAnimationObject CurrentAnimation;
    public EyeAnimationObject LastAnimation;

    private Queue<EyeAnimationObject> AnimationQueue;

    public void AddToQueue(String animation, String name, String position, boolean isIntermediateState) {
        this.AddToQueue(animation, name, position, isIntermediateState, 250);
    }

    public void AddToQueue(String animation, String name, String position, boolean isIntermediateState, int minDelayAfterAnimation) {
        if (name.equals("blink")
                && GetQueueSize() > 0
                && this.LastAnimation != null
                && this.LastAnimation.AnimationName.equals("blink"))
            return;
        Log.w(TAG, animation);
        EyeAnimationObject animationObject = new EyeAnimationObject();
        animationObject.AnimationObject = animation;
        animationObject.AnimationName = name;
        animationObject.IntermediateAnimation = isIntermediateState;
        animationObject.Position = position;
        animationObject.MinDelayAfterAnimation = minDelayAfterAnimation;

        this.AnimationQueue.add(animationObject);

        this.LastAnimation = animationObject;
    }

    public EyeAnimationObject GetFromQueue() {
        EyeAnimationObject animationObject = this.AnimationQueue.poll();
        this.CurrentAnimation = animationObject;

        return animationObject;
    }

    public EyeAnimationObject PeekAtQueue() {
        return this.AnimationQueue.peek();
    }

    public int GetQueueSize() {
        return this.AnimationQueue.size();
    }

    public void ClearQueue() {
        this.AnimationQueue.clear();
    }

    private EyeState() {
        AnimationRunning = false;
        Loop = false;
        AnimationEndTimestamp = SystemClock.uptimeMillis();

        IdleMode = false;
        IdleDelay = 0;

        AnimationQueue = new LinkedList<EyeAnimationObject>();
    }
}
