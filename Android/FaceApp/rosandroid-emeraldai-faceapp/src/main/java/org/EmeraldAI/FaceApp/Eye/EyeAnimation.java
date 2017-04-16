package org.EmeraldAI.FaceApp.Eye;

import java.util.Arrays;
import java.util.List;

/**
 * Created by maximilianporzelt on 15.04.17.
 */

public class EyeAnimation {

    private List<String> _position = Arrays.asList("center","left","right","top","bottom");
    private List<String> _availableAnimationPosition = Arrays.asList("center","left","right");
    private List<String> _animation = Arrays.asList("blink","bad","doubt","sad","shock");


    public void TriggerAnimation(String command)
    {
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

        // TODO: one needs to be center

        String gifToPlay = String.format("move_{0}_{1}", EyeState.getInstance().LastQueuedPosition, destination);
        EyeState.getInstance().AddToQueue(gifToPlay, "move", destination, false);
    }

    public void PlayAnimation(String animation)
    {
        // Example: center_bad_end
        String state = "start";
        if(EyeState.getInstance().LastQueuedIsIntermediateState)
        {
            state = "end";
        }

        String position = EyeState.getInstance().LastQueuedPosition;

        // If current position has no animations reset to center
        if(!_availableAnimationPosition.contains(position))
        {
            position = "center";
            this.MoveTo("center");
        }

        String gifToPlay = String.format("{0}_{1}_{2}", position, animation, state);
        EyeState.getInstance().AddToQueue(gifToPlay, animation, position, (state.equals("start")));
    }

    public void ResetAnimation()
    {
        // TODO: reset animation and go back to default

        EyeState es = EyeState.getInstance();
        EyeAnimationObject currentAnimation =  es.CurrentAnimation;

        // TODO: get currentposition + is intermediate
        // TODO: calculate next to reset

        es.ClearQueue();

    }
}
