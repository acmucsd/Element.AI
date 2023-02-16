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
    // public Environment envConfig;

    public String act() throws JsonProcessingException {
        return "{\"turn\": 0}";
    }

}