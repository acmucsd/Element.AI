package com.elementai;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.elementai.element.Player;

import java.util.Map;
// import com.elementai.objectmapper.Mapper;

// import java.util.Random;

public class Agent {    
    public final int TEMP = -1;
    public final int UNOCCUPIED = 0;
    public final int TAIL = 1;
    public final int TERRITORY = 2;
    public final int BOMB = 3;
    public final int BOOST = 4;


    public int iter;
    public int currStep;
    public int remainingOverageTime;
    public String player;

    public Map<String, Player> obs;
    public int[][] boardState;
    public int[][] playersState;

    public Map<String, Integer> rewards;

    private int timesMoved = 0;

    public String act() throws JsonProcessingException {

        /* -----------------------------------------------------
         * DO NOT CHANGE ANY CODE ABOVE THIS LINE
         */ 


        /*
         * YOUR BOT GOES HERE. Remember to set turn = -1, 0, or 1
         */

        Player p = obs.get(player);

        // if we are not allowed to go, don't waste time computing
        if (p.speed <= currStep || p.resetting)
            return formatAction(0);

        // bot makes a simple square and stays in it
        int turn = timesMoved != 0 ? timesMoved % 10 == 0 ? 1 : 0 : 0;

        timesMoved++;

        // NOTE: ALWAYS use formatAction() when returning a turn value
        return formatAction(turn);
    }

    public String formatAction(int turn) {
        return "{\"turn\": " + turn + "}";
    }

}