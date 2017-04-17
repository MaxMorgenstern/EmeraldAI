package org.EmeraldAI.FaceApp.Eye;

import android.os.SystemClock;
import android.util.Log;

import org.apache.commons.lang.ObjectUtils;

import java.text.MessageFormat;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

import static android.content.ContentValues.TAG;

/**
 * Created by maximilianporzelt on 15.04.17.
 */

public class EyeAnimation {

    private List<String> _position = Arrays.asList("center","left","right","top","bottom");
    private List<String> _availableAnimationPosition = Arrays.asList("center","left","right");
    private List<String> _animation = Arrays.asList("blink","bad","doubt","sad","shock");
    private List<String> _singleAnimation = Arrays.asList("blink");
    private String _defaultLocation = "center";

    public void TriggerAnimation(String command)
    {
        if(EyeState.getInstance().IdleMode)
        {
            this.ResetAnimation(true);
            EyeState.getInstance().IdleMode = false;
        }

        if (_position.contains(command))
        {
            this.MoveTo(command);
        }

        if (_animation.contains(command))
        {
            this.PlayAnimation(command);
        }

        // TODO: throw error
    }

    public void MoveTo(String destination)
    {
        // Example: move_right_center
        EyeState es = EyeState.getInstance();
        EyeAnimationObject eao = es.LastAnimation;

        String position = "center";
        if (eao != null)
        {
            if (eao.Position.equals(destination))
                return;

            if (!eao.Position.equals(_defaultLocation) && !destination.equals(_defaultLocation))
            {
                this.MoveTo(_defaultLocation);
                eao = es.LastAnimation;
            }
            position = eao.Position;
        }

        String gifToPlay = MessageFormat.format("move_{0}_{1}", position, destination);
        es.AddToQueue(gifToPlay, "move", destination, false);
    }

    public void PlayAnimation(String animation)
    {
        // Example: center_bad_end
        EyeState es = EyeState.getInstance();
        EyeAnimationObject eao = es.LastAnimation;

        String position = "center";
        String state = "end";

        if (eao != null)
        {
            if (eao.IntermediateAnimation && !eao.AnimationName.equals(animation))
            {
                this.PlayAnimation(eao.AnimationName);
            }

            state = (eao.IntermediateAnimation) ? "end" : "start";
            if (_singleAnimation.contains(animation))
            {
                state = "full";
            }

            position = eao.Position;
        }

        // If current position has no animations reset to center
        if(!_availableAnimationPosition.contains(position))
        {
            position = _defaultLocation;
            this.MoveTo(_defaultLocation);
        }

        String gifToPlay = MessageFormat.format("{0}_{1}_{2}", position, animation, state);
        es.AddToQueue(gifToPlay, animation, position, (state.equals("start")));
    }

    public void ResetAnimation()
    {
        this.ResetAnimation(false);
    }

    public void ResetAnimation(boolean movePositionToDefault)
    {
        EyeState es = EyeState.getInstance();
        es.ClearQueue();

        EyeAnimationObject currentAnimation =  es.CurrentAnimation;

        if(currentAnimation.IntermediateAnimation)
        {
            String gifToPlay = MessageFormat.format("{0}_{1}_{2}", currentAnimation.Position, currentAnimation.AnimationName, "end");
            es.AddToQueue(gifToPlay, currentAnimation.AnimationName, currentAnimation.Position, false, 0);
        }

        if(movePositionToDefault && !currentAnimation.Position.equals(_defaultLocation))
        {
            this.MoveTo(_defaultLocation);
        }
    }

    public void EnableIdleMode()
    {
        EyeState es = EyeState.getInstance();

        long timeToWaitUntilIdleBegins = 5000; // TODO

        if(es.GetQueueSize() > 0 || es.AnimationRunning)
            return;

        long now = SystemClock.uptimeMillis();
        if(!es.IdleMode && (es.AnimationEndTimestamp + timeToWaitUntilIdleBegins) >= now)
            return;

        if(es.IdleMode && (es.AnimationEndTimestamp + es.IdleDelay) >= now)
            return;

        es.IdleMode = true;

        int max = 15000; // TODO
        int min = 5000; // TODO
        es.IdleDelay = new Random().nextInt(max - min + 1) + min;

        String moveToPosition = _position.get(new Random().nextInt(_position.size()));
        this.MoveTo(moveToPosition);
    }
}
