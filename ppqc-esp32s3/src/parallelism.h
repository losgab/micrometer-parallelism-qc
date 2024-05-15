/**
 * Parallelism Measurement Jig for Build Platforms
 * 
 * 
 * @author Gabriel Thien @ Zydex (Asiga 3D Printers)
*/
#pragma once

#define MAX_MICROMETERS 16

typedef struct parallelism {
    float micrometer_data[MAX_MICROMETERS];
    float parallelism_score;
    criteria_grade_t grade;
} parallelism_t;

typedef enum CriteriaConstants
{
    NONE_TRUE,
    PARALELLISM_TRUE_ONLY,
    PROFILE_NOM_TRUE_ONLY,
    BOTH_TRUE,
    ERROR
} criteria_grade_t;
