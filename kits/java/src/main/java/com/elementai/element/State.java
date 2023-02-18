package com.elementai.element;
import java.util.Map;

public class State {

    public Player player0;
    public Player player1;
    public Player player2;
    public Player player3;

    public int iteration;
    public int currStep;
    public int remainingOverageTime;
    public String player;

    public Map<String, Integer> rewards;

    public int[][] boardState;
    public int[][] playersState;
}
