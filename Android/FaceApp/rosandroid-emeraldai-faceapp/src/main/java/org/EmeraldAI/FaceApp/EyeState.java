package org.EmeraldAI.FaceApp;

/**
 * Created by maximilianporzelt on 15.04.17.
 */

public class EyeState {
    private static final EyeState ourInstance = new EyeState();

    public static EyeState getInstance() {
        return ourInstance;
    }

    // TODO - update eye state
    public String CurrentPosition; // Left Center Right
    public boolean IntermediateState;
    public boolean AnimationRunning;
    public boolean Loop;

    private EyeState() { }
}
