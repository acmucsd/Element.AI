package com.elementai.element;
import java.util.Map;

public class State {

    public Obs obs;

    public int iter;
    public int currStep;
    public int remainingOverageTime;
    public String player;

    public Map<String, Integer> rewards;

    public int[][] boardState;
    public int[][] playersState;
}
