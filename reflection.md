## Brief description of approach

For this challenge, I really wanted to explore the capabilities of Cursor and its Composer 1 agent. For work, I use Roo Code a lot (with Claude Sonnet 4.5 managed in AWS Bedrock), but primarily in Architect mode for onboarding to new code bases and for planning and iterating through designs. I still write 75% of my application code, but use Roo in Code mode for writing nearly all automated tests.

So today, I really wanted to have the Composer 1 agent write the majority of the application and test code to see how powerful it could be and how that dev work flow would feel. Overall, I was quite impressed with what it produced!

I would say the other thing I was trying to emphasize was having clear interfaces between each part of the system (game engine, storage service, and the game AI). This way each item was loosely coupled and would allow for easy swapping of implementations (ex: could build a JSON file storage service or a minimax algorith for the game AI).

## Which AI tools were used

1. Cursor with its Composer 1 agent for code generation & some discussion on system design
2. Cursor with GPT-5.1 Codex High as a code reviewer/evaluator
3. Google Gemini for more general questions not necessarily needing the context of this application

## Anything that didn’t go as planned or you'd improve with more time

1. I probably should've discussed the data model and the system design here with the available cursor agents to refine things before having it build out the models, storage layer, etc. Overall, I think the data model is decent and allows for flexibility for future iterations like computer vs computer, human vs human, expanding to a 4x4 board, etc. Mostly, I wanted these higher-level decisions to be purely mine for the sake of the challenge, but I'm sure there would be plenty to improve here through discussion with the Cursor agents.

2. I was debating on how I represented the board using the coordinates A1, A2, A3... instead of a 2D or 1D array. That decision introduced some extra translation from A1 into (0,0) coordinates, which was probably unnecessary. I think if I had re-done things, I would have kept the game engine logic based on a 3x3 matrix, and just had a translation layer that would turn the A1, A2 notation into the appropriate indices. Or, I could have just had the user enter the indices in the first place (I just felt that the A1, B2, C3 naming would be more intuitive to people).

3. Definitely would have added more unit tests for the game engine and AI modules. I should've added these earlier and read through the Cursor-generated code more thoroughly. I think mostly I wanted to get the MCP server working first (and I was probably trusting Cursor too much), so I neglected the unit tests a bit.

4. There are several items I would like to refactor, but ran out of time. I think the list of issues that the evaluator agent came up with was quite insightful. I think some TODO items would include:
    - Create a constants file for things like VALID_POSITIONS (which was repeated in several modules)
    - Remove redundant sorting of the list of moves (should already be sorted after insertion)
    - I believe we can just return the Pydantic models in the tools and clients would know how to deserialize that into JSON
    - Evaluate bug on no turn-order or player-validation in the `add_move` tool
    - Evaluate bug that players could share the same piece 
    - Evaluate bug that `get_next_move` tool has no validation that checks that the player exists in the current game instance