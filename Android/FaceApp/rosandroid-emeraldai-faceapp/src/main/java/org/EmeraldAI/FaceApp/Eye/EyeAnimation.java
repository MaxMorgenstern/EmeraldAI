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
    private List<String> _singleAnimation = Arrays.asList("blink");
    private String _defaultLocation = "center";

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
        EyeState es = EyeState.getInstance();

        if(es.LastAnimation.Position.equals(destination))
            return;

        if (!es.LastAnimation.Position.equals(_defaultLocation) && !destination.equals(_defaultLocation))
        {
            this.MoveTo(_defaultLocation);
        }

        String gifToPlay = String.format("move_{0}_{1}", es.LastAnimation.Position, destination);
        es.AddToQueue(gifToPlay, "move", destination, false);
    }

    public void PlayAnimation(String animation)
    {
        // Example: center_bad_end
        EyeState es = EyeState.getInstance();
        EyeAnimationObject eao = es.LastAnimation;


        if(eao.IntermediateAnimation && !eao.AnimationName.equals(animation))
        {
            this.PlayAnimation(eao.AnimationName);
        }

        String state = (eao.IntermediateAnimation) ? "end" : "start";
        if(_singleAnimation.contains(animation))
        {
            state = "full";
        }

        String position = eao.Position;

        // If current position has no animations reset to center
        if(!_availableAnimationPosition.contains(position))
        {
            position = _defaultLocation;
            this.MoveTo(_defaultLocation);
        }

        String gifToPlay = String.format("{0}_{1}_{2}", position, animation, state);
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
            String gifToPlay = String.format("{0}_{1}_{2}", currentAnimation.Position, currentAnimation.AnimationName, "end");
            es.AddToQueue(gifToPlay, currentAnimation.AnimationName, currentAnimation.Position, false, 0);
        }

        if(movePositionToDefault && !currentAnimation.Position.equals(_defaultLocation))
        {
            this.MoveTo(_defaultLocation);
        }
    }
}
