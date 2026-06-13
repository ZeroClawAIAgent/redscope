package com.redscope;

import net.fabricmc.api.ClientModInitializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * RedScope Client - Client-side initialization
 */
public class RedScopeClientMod implements ClientModInitializer {
    public static final Logger LOGGER = LoggerFactory.getLogger(RedScopeMod.MOD_ID);

    @Override
    public void onInitializeClient() {
        LOGGER.info("RedScope client initialized!");
        
        // TODO: Initialize client-side features
        // - Overlay rendering
        // - HUD elements
        // - Keybindings
    }
}