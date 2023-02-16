package com.elementai;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.elementai.objectmapper.Mapper;

import java.io.IOException;
import java.util.Scanner;

/**
 * Main class
 * Element-AI-2023
 */
public class Bot
{
    public static void main( String[] args ) throws IOException {
        Agent agent = new Agent();
        Scanner scanner = new Scanner(System.in);
        while (true) {
            String jsonIn = scanner.nextLine();             // Read input
            String jsonOut = processing(agent, jsonIn);     // Main function
            System.out.println(jsonOut);                    // Output command
        }
    }

    public static String processing(Agent agent, String json) throws JsonProcessingException {
        System.err.println("hi");
        Mapper.updateState(agent, json);            // Update state
        String jsonAction = null;
        // if (agent.obs.realEnvSteps < 0) {
        //     // Do nothing
        // }
        // else {
        //     jsonAction = agent.act();
        // }
        jsonAction = agent.act();
        // if (jsonAction == null) {
        //     ObjectMapper objectMapper = new ObjectMapper();
        //     jsonAction = objectMapper.createObjectNode().toString();
        // }
        System.err.println(jsonAction);
        return jsonAction;
    }
}