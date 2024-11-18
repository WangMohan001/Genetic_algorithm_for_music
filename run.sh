#!/bin/bash

CONFIG_PATH="genetic/configs/config_algorithm.json"
SOUND_FONT="genetic/soundfronts/27.3mg_symphony_hall_bank.SF2"
OUTPUT_MIDI="output/result.midi"
OUTPUT_AUDIO="output/result.wav"
INSTRUMENT="violin"
INSTRUMENT_JSON_PATH="genetic/configs/instruments.json"

echo "Using config file: $CONFIG_PATH"
echo "Sound font file: $SOUND_FONT"
echo "Output MIDI file: $OUTPUT_MIDI"
echo "Output audio file: $OUTPUT_AUDIO"
echo "Instrument used: $INSTRUMENT"
echo "Instrument JSON path: $INSTRUMENT_JSON_PATH"

python -m genetic.main "$CONFIG_PATH" "$SOUND_FONT" "$OUTPUT_MIDI" "$OUTPUT_AUDIO" "$INSTRUMENT" "$INSTRUMENT_JSON_PATH"
 