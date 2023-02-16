package com.elementai;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.elementai.element.Obs;
// import com.elementai.objectmapper.Mapper;

// import java.util.Random;

public class Agent {

    // private final Random random = new Random(2022);

    public Obs obs;
    public int iter;
    public int currStep;
    public int remainingOverageTime;
    public String player;

    public int[][] boardState;
    public int[][] playersState;

    public String act() throws JsonProcessingException {

        // System.err.println(iter);

        int turn = iter != 0 ? iter % 10 == 0 ? 1 : 0 : 0;

        return "{\"turn\": " + turn + "}";
    }

}