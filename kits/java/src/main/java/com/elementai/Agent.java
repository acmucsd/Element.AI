package com.elementai;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.elementai.element.Player;

import java.util.Map;
// import com.elementai.objectmapper.Mapper;

// import java.util.Random;

public class Agent {    
    public int iter;
    public int currStep;
    public int remainingOverageTime;
    public String player;

    public Map<String, Player> obs;
    public int[][] boardState;
    public int[][] playersState;

    public Map<String, Integer> rewards;

    public String act() throws JsonProcessingException {

        /* -----------------------------------------------------
         * DO NOT CHANGE ANY CODE ABOVE THIS LINE
         */ 


        /*
         * YOUR BOT GOES HERE. Remember to set turn = -1, 0, or 1
         */

        int speed = obs.get(player).speed;

        if (speed <= currStep)
            return formatAction(0);

        int turn = iter != 0 ? iter % 10 == 0 ? 1 : 0 : 0;

        // NOTE: ALWAYS use formatAction() when returning a turn value
        return formatAction(turn);
    }

    public String formatAction(int turn) {
        return "{\"turn\": " + turn + "}";
    }

}