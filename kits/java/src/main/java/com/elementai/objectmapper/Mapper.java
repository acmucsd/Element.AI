package com.elementai.objectmapper;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.elementai.Agent;
import com.elementai.element.State;

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
        System.err.println(json);
        if (agent.obs == null) {

            State state = objectMapper.readValue(json, State.class);
            agent.obs = state.obs;
            agent.iter = state.iter;
            agent.currStep = state.currStep;
            agent.remainingOverageTime = state.remainingOverageTime;
            agent.player = state.player;
        }
        else {
            State state = objectMapper.readValue(json, State.class);
            agent.iter = state.iter;
            agent.remainingOverageTime = state.remainingOverageTime;
            agent.obs.playerData = state.obs.playerData;
            agent.obs.realEnvSteps = state.obs.realEnvSteps;
        }
    }

}