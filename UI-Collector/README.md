## This project implements automatic traversal of mobile applications based on uiautomator2

## Environment Configuration

Setting up uiautomator2 environment: https://github.com/openatx/uiautomator2

Setting up tesseract environment, also requires configuring the Chinese language pack:  https://github.com/tesseract-ocr/tesseract

Change the system encoding to utf-8 instead of gbk

## Running

Modify the package name and app name to be tested in apk_pkgName.txt, format as package name | app name. Supports batch analysis. Ensure there is a space on both sides of |.
In the config_settings dictionary in test_integrate.py, you can set the traversal depth, with the corresponding key as 'dynamic_ui_depth'.

There are also advanced configurations that can be modified in Config.py. If modification is needed, make sure to only change the marked parts.
Run `python run_config.py`

## Traversal Process

### Click Process

For a screen, it will sequentially click on all clickable components of the current screen.
Since clicking may lead to reaching a new screen, it is necessary to maintain the context of the current screen before clicking,
such as screen information (text, position), which components have been clicked on the current screen...

Upon reaching a new screen, the screen information (text, component position, etc.) of the current screen and the Memory (storing previously traversed screen information)
are compared for similarity. If the similarity is greater than a threshold, the current screen is considered an existing screen (ExistScreen), otherwise, it is considered a new screen (NewScreen).
After extracting the context of the current screen, continue clicking from where the previous unfinished clicks left off. If the current screen has been fully clicked, trigger
press back to return to the previous screen to continue clicking, repeating the above process.

Definition of a screen being fully clicked: All clickable components on that screen are clicked
Definition of a clickable component being fully clicked: The component does not lead to a page transition, or the component's corresponding next screen click is completed

### State Detection

The following states are defined:

| State                   | Description                                            | Action Taken                                                 |
| ----------------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| STATE_ExitApp           | The test app has been exited                           | press back to return to the test app                         |
| STATE_InputMethod       | Encountered an input method                            | press back to exit the input method                          |
| STATE_ExistScreen       | The current screen already exists                      | Extract the context of the current screen and continue clicking |
| STATE_FinishScreen      | Current screen click completed                         | press back to return to the previous screen                  |
| STATE_NewScreen         | Current screen is a newly reached screen               | Allocate context for the new screen, add it to the App screen transition graph, and start clicking |
| STATE_PermissonScree    | Current screen is a system permission screen           | Random clicking strategy                                     |
| STATE_HomeScreenRestart | The current screen is stuck                            | Restart the app                                              |
| STATE_Back              | The current screen is an ErrorScreen or exceeded depth | press back to exit the current screen                        |

## Features

### Hierarchical Traversal

Due to the complexity of commercial apps, there may be hundreds of activities and thousands of screens, and users may not necessarily be concerned with very deep screens. Therefore, support for
user-configurable traversal depth MaxDepth; the tool will start traversing from level 1, only traversing the first level, and when the traversal of the first level screens is complete, the level is increased to 2... continuously traversing
until all screens up to the configured depth are covered.

### Handling of Activity-embedded Fragments, Menus, Drawers

Activities consist of Fragments, Menus, Drawers, etc. Activities are represented as a stack, but an Activity may contain multiple Fragments, each representing a different screen, and Fragments may not necessarily be stack-based
(depends on the developer's design). Therefore, using DFS (stack) to simulate screen behavior can be difficult.

Approach: We use a finite state machine model (FSM) to simulate screen behavior. This is combined with restart app and loop detection strategies to ensure complete coverage of all Fragments, Menus, Dialogs, and Drawers scenarios.

### Handling of Pop-up Windows (Dialogs, Popup Windows)

App often pops up dialog boxes, which, if not dismissed, persist and hinder the normal operation of traversal testing, even causing the testing process to get stuck. Moreover, these dialog boxes not only appear during the process of clicking components but also when navigating back using the press back operation.

Approach: Utilize two YOLOv5 object detection models. Firstly, Model 1 detects if the current screen is a popup window. If the current screen is identified as a popup window, Model 2 is employed to detect the position information of clickable options on the current popup window for interaction.

### Screen Deduplication

As elements on the same screen in an app may undergo slight changes, it is crucial to deduplicate screens and consider screens with minor changes as identical screens rather than entirely new ones.

Approach: Upon reaching a new screen, the UID of the current screen (concatenation of text and position information of clickable components) is compared for similarity with the Memory (storing all previously traversed screen UIDs). If the similarity exceeds a certain threshold (90%), the current screen is deemed an existing screen. In such cases, the context of the screen is extracted to continue interactions.

When screen elements change, it often involves adding or removing certain components or alterations in text/position information. To address this, the similarity comparison algorithm employed is the Longest Common Subsequence (LCS) algorithm, without the need to consider the specifics of the string's semantic information (NLP-related algorithms are not used).

### Enhancing Coverage

Restricting each component to be clicked only once may lead to many screens being left untraversed. Hence, the program tracks the next screen each clickable component leads to. If the next screen has not been fully interacted with, clicking the component will redirect to the next screen for further interactions. Additionally, checks for back edges/loops are in place to avoid getting stuck in infinite loops.

### Fault Tolerance Mechanisms

When navigating back to the previous screen using the press back operation, scenarios like encountering popups or ineffective back navigation may impede the tool's continued traversal. In such cases, the program triggers:

1. A random clicking mechanism, where a component that may trigger a screen transition is randomly selected and clicked.
2. If back navigation remains ineffective, the testing app is restarted. The program also logs the frozen screen and the component clicked to reach that screen to prevent reclicking after the restart.

### App Screen Transition Graph Generation

The tool records the screen transition graph and screenshots of the app traversal process. Upon completion, it outputs a screen transition graph composed of screen captures and transition arrows.

