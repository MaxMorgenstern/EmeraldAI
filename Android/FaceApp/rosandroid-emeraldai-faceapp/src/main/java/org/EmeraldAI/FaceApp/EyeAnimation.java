package org.EmeraldAI.FaceApp;

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

        // error
    }

    public void MoveTo(String destination)
    {
        // Example: move_right_center
        String gifToPlay = String.format("move_{0}_{1}", EyeState.getInstance().CurrentPosition, destination);
        // TODO: 16.04.17  - Trigger animation
    }

    public void PlayAnimation(String animation)
    {
        // Example: center_bad_end

        String state = "start";
        if(EyeState.getInstance().IntermediateState)    // TODO - if we use an animation queue this needs to be updated
        {
            state = "end";
        }

        String position = EyeState.getInstance().CurrentPosition; // TODO - if we use an animation queue this needs to be updated

        // If current position has no animations reset to center
        if(!_availableAnimationPosition.contains(position))
        {
            position = "center";
            this.MoveTo("center");
        }


        String gifToPlay = String.format("{0}_{1}_{2}", position, animation, state);
        // TODO: 16.04.17  - Trigger animation
    }
}
