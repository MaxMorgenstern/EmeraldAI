package org.EmeraldAI.FaceApp.Eye;

import java.util.LinkedList;
import java.util.Queue;

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

    public EyeAnimationObject CurrentAnimation;
    public EyeAnimationObject LastAnimation;

    private Queue<EyeAnimationObject> AnimationQueue = new LinkedList<EyeAnimationObject>();

    public void AddToQueue(String animation, String name, String position, boolean isIntermediateState)
    {
        this.AddToQueue(animation, name, position, isIntermediateState, 500);
    }

    public void AddToQueue(String animation, String name, String position, boolean isIntermediateState, int delayAfterAnimation)
    {
        EyeAnimationObject animationObject = new EyeAnimationObject();
        animationObject.AnimationObject = animation;
        animationObject.AnimationName = name;
        animationObject.IntermediateAnimation = isIntermediateState;
        animationObject.Position = position;
        animationObject.MinDelayAfterAnimation = delayAfterAnimation;

        this.AnimationQueue.add(animationObject);

        this.LastAnimation = animationObject;
    }

    public EyeAnimationObject GetFromQueue()
    {
        EyeAnimationObject animationObject = this.AnimationQueue.poll();
        this.CurrentAnimation = animationObject;

        return animationObject;
    }

    public EyeAnimationObject PeekAtQueue()
    {
        return this.AnimationQueue.peek();
    }

    public int GetQueueSize()
    {
        return this.AnimationQueue.size();
    }

    public void ClearQueue()
    {
        this.AnimationQueue.clear();
    }

    private EyeState() { }
}
