package org.EmeraldAI.FaceApp.Eye;

import android.os.SystemClock;
import android.util.Log;

import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

import static android.content.ContentValues.TAG;

/**
 * Created by maximilianporzelt on 15.04.17.
 */

public class EyeAnimation {

    private List<String> _position;
    private List<String> _availableAnimationPosition;
    private List<String> _animation;
    private List<String> _singleAnimation;
    private String _defaultLocation;

    private int _intermediate_timeout = 30;
    private int _blink_percentage = 97;
    private boolean _enable_idle_mode = true;
    private int _time_to_wait_until_idle_begins = 60;
    private int _min_animation_delay = 1;
    private int _max_animation_delay = 30;

    public EyeAnimation() {
        _position = Arrays.asList("center", "left", "right", "top", "bottom");
        _availableAnimationPosition = Arrays.asList("center", "left", "right");
        _animation = Arrays.asList("blink", "bad", "doubt", "sad", "shock");
        _singleAnimation = Arrays.asList("blink");
        _defaultLocation = "center";
    }

    public void TriggerAnimation(String command) {
        if (EyeState.getInstance().IdleMode) {
            this.ResetAnimation(true);
            EyeState.getInstance().IdleMode = false;
        }

        if (_position.contains(command)) {
            this.MoveTo(command);
            return;
        }

        if (_animation.contains(command)) {
            this.PlayAnimation(command);
            return;
        }

        Log.e(TAG, "TriggerAnimation(): Invalid command received: " + command);
    }

    public void MoveTo(String destination) {
        // Example: move_right_center
        EyeState es = EyeState.getInstance();
        EyeAnimationObject eao = es.LastAnimation;

        String position = "center";
        if (eao != null) {
            if (eao.Position.equals(destination))
                return;

            if (!eao.Position.equals(_defaultLocation) && !destination.equals(_defaultLocation)) {
                this.MoveTo(_defaultLocation);
                eao = es.LastAnimation;
            }
            position = eao.Position;
        }

        String gifToPlay = MessageFormat.format("move_{0}_{1}", position, destination);
        es.AddToQueue(gifToPlay, "move", destination, false);
    }

    public void PlayAnimation(String animation) {
        // Example: center_bad_end
        EyeState es = EyeState.getInstance();
        EyeAnimationObject eao = es.LastAnimation;

        String position = "center";
        String state = "start";

        if (eao != null) {
            if (eao.IntermediateAnimation && !eao.AnimationName.equals(animation)) {
                this.PlayAnimation(eao.AnimationName);
            }

            state = (eao.IntermediateAnimation) ? "end" : "start";
            position = eao.Position;
        }

        if (_singleAnimation.contains(animation)) {
            state = "full";
        }

        // If current position has no animations reset to center
        if (!_availableAnimationPosition.contains(position)) {
            position = _defaultLocation;
            this.MoveTo(_defaultLocation);
        }

        String gifToPlay = MessageFormat.format("{0}_{1}_{2}", position, animation, state);
        es.AddToQueue(gifToPlay, animation, position, (state.equals("start")));
    }

    public void ResetAnimation() {
        this.ResetAnimation(false);
    }

    public void ResetAnimation(boolean movePositionToDefault) {
        EyeState es = EyeState.getInstance();
        es.ClearQueue();

        EyeAnimationObject currentAnimation = es.CurrentAnimation;

        if (currentAnimation.IntermediateAnimation) {
            String gifToPlay = MessageFormat.format("{0}_{1}_{2}", currentAnimation.Position, currentAnimation.AnimationName, "end");
            es.AddToQueue(gifToPlay, currentAnimation.AnimationName, currentAnimation.Position, false, 0);
        }

        if (movePositionToDefault && !currentAnimation.Position.equals(_defaultLocation)) {
            this.MoveTo(_defaultLocation);
        }
    }


    public void BlinkUpdater() {
        EyeState es = EyeState.getInstance();
        long now = SystemClock.uptimeMillis();

        if (es.GetQueueSize() > 1 || es.AnimationRunning
                || (es.CurrentAnimation != null && es.CurrentAnimation.IntermediateAnimation &&
                (es.AnimationEndTimestamp + (_intermediate_timeout * 1000)) >= now))
            return;

        if (new Random().nextInt(100 + 1) > _blink_percentage)
            this.PlayAnimation("blink");
    }

    public void IdleUpdater() {
        if (!_enable_idle_mode)
            return;

        EyeState es = EyeState.getInstance();
        long now = SystemClock.uptimeMillis();

        if (es.GetQueueSize() > 0)
            return;

        // wait x seconds since last animation to start idle
        if (!es.IdleMode && (es.AnimationEndTimestamp + (_time_to_wait_until_idle_begins * 1000)) >= now)
            return;

        if (es.IdleMode && (es.AnimationEndTimestamp + es.IdleDelay) >= now)
            return;

        if (!es.IdleMode)
            this.ResetAnimation();
        es.IdleMode = true;

        int max = _max_animation_delay * 1000;
        int min = _min_animation_delay * 1000;
        es.IdleDelay = new Random().nextInt(max - min + 1) + min;

        List<String> combinedList = new ArrayList<String>();
        combinedList.addAll(_availableAnimationPosition);
        combinedList.addAll(_position);

        String moveToPosition = combinedList.get(new Random().nextInt(combinedList.size()));
        this.MoveTo(moveToPosition);

    }
}
