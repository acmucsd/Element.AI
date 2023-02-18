package com.elementai.objectmapper;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.HashMap;
import java.util.Map;

import com.elementai.Agent;
import com.elementai.element.State;
import com.elementai.element.Player;

public class Mapper {

    public static String getJson(Object object) throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();
        return objectMapper.writeValueAsString(object);
    }

    public static void updateState(Agent agent, String json) throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
        
        State state = objectMapper.readValue(json, State.class);

        Player[] arr = { state.player0, state.player1, state.player2, state.player3 };

        Map<String, Player> obs = new HashMap<String, Player>();
        
        for (int i = 0; i < arr.length; ++i)
            if (arr[i] != null)
                obs.put("player_" + i, arr[i]);

        agent.obs = obs;
        
        agent.rewards = state.rewards;

        agent.iter = state.iter;
        agent.currStep = state.currStep;
        agent.remainingOverageTime = state.remainingOverageTime;
        agent.player = state.player;

        agent.boardState = state.boardState;
        agent.playersState = state.playersState;
    }

}