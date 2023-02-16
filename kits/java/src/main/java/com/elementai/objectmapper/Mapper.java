package com.elementai.objectmapper;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.elementai.Agent;
import com.elementai.element.State;
import com.elementai.element.Player;
// import com.elementai.element.Obs;
// import com.elementai.element.Board;

// import java.util.Map;

public class Mapper {

    public static String getJson(Object object) throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();
        return objectMapper.writeValueAsString(object);
    }

    public static void updateState(Agent agent, String json) throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
        // check first step
        // System.err.println(json);
        
        State state = objectMapper.readValue(json, State.class);

        Player player0 = state.player0;
        Player player1 = state.player1;
        Player player2 = state.player2;
        Player player3 = state.player2;
        
        agent.rewards = state.rewards;

        agent.iter = state.iter;
        agent.currStep = state.currStep;
        agent.remainingOverageTime = state.remainingOverageTime;
        agent.player = state.player;

        agent.boardState = state.boardState;
        agent.playersState = state.playersState;
    }

}