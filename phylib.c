#include <stdlib.h>
#include <string.h>
#include <math.h>
///////////////////////////////////////////////////////////////////////////////////////////////////
#include "phylib.h"
///////////////////////////////////////////////////////////////////////////////////////////////////

#define DIV(x, y) ((y == 0) ? 0 : x/y) //? set to 0 instead of NaN

///////////////////////////////////////////////////////////////////////////////////////////////////

phylib_object * phylib_new_still_ball(
        unsigned char number,
        phylib_coord * pos
        )
{
    // Allocate memory for a new phylib_object
    phylib_object * new_object = calloc(1, sizeof(phylib_object));

    // If malloc fails, return NULL
    if (new_object == NULL) {
        return NULL;
    }
    memset(new_object, 0, sizeof(phylib_object));

    // Set the type to PHYLIB_STILL_BALL
    new_object->type = PHYLIB_STILL_BALL;

    // Transfer the information provided in the function parameters into the structure
    new_object->obj.still_ball.number = number;

    if (pos) {
        new_object->obj.still_ball.pos.x = pos->x;
        new_object->obj.still_ball.pos.y = pos->y;
    }

    // Return a pointer to the phylib_object
    return new_object;
}

///////////////////////////////////////////////////////////////////////////////////////////////////

phylib_object * phylib_new_rolling_ball(
        unsigned char number,
        phylib_coord * pos,
        phylib_coord * vel,
        phylib_coord * acc
        )
{
    // Allocate memory for a new phylib_object
    phylib_object * new_object = calloc(1, sizeof(phylib_object));

    // If malloc fails, return NULL
    if (new_object == NULL) {
        return NULL;
    }
    memset(new_object, 0, sizeof(phylib_object));

    // Set the type to PHYLIB_ROLLING_BALL
    new_object->type = PHYLIB_ROLLING_BALL;

    // Transfer the information provided in the function parameters into the structure
    new_object->obj.rolling_ball.number = number;
    if (pos) {
        new_object->obj.rolling_ball.pos.x = pos->x;
        new_object->obj.rolling_ball.pos.y = pos->y;
    }
    if (vel) {
        new_object->obj.rolling_ball.vel.x = vel->x;
        new_object->obj.rolling_ball.vel.y = vel->y;
    }
    if (acc) {
        new_object->obj.rolling_ball.acc.x = acc->x;
        new_object->obj.rolling_ball.acc.y = acc->y;
    }

    // Return a pointer to the phylib_object
    return new_object;
}

///////////////////////////////////////////////////////////////////////////////////////////////////

phylib_table * phylib_new_table(
        void
        )
{
    // Allocate memory for a new phylib_table
    phylib_table * new_table = calloc(1, sizeof(phylib_table));

    // If malloc fails, return NULL
    if (new_table == NULL) {
        return NULL;
    }

    // Set the time to 0.0
    new_table->time = 0.0;

    // Initialize all pointers in the object array to NULL
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        new_table->object[i] = NULL;
    }

    // Add the cushions and holes to the table
    // Note: You'll need to implement the phylib_new_hcushion, phylib_new_vcushion, and phylib_new_hole functions
    new_table->object[0] = phylib_new_hcushion(0.0);
    new_table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);

    new_table->object[2] = phylib_new_vcushion(0.0);
    new_table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    // Add the holes here...

    // Add holes at the four corners
    // Add two more holes midway between the top and bottom holes

    phylib_coord holePos1 = {0.0               , 0.0};
    phylib_coord holePos2 = {0.0               , PHYLIB_TABLE_LENGTH/2};
    phylib_coord holePos3 = {0.0               , PHYLIB_TABLE_LENGTH};

    phylib_coord holePos4 = {PHYLIB_TABLE_WIDTH, 0.0};
    phylib_coord holePos5 = {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH/2};
    phylib_coord holePos6 = {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH};

    new_table->object[4] = phylib_new_hole(& holePos1);
    new_table->object[5] = phylib_new_hole(& holePos2);
    new_table->object[6] = phylib_new_hole(& holePos3);
    new_table->object[7] = phylib_new_hole(& holePos4);
    new_table->object[8] = phylib_new_hole(& holePos5);
    new_table->object[9] = phylib_new_hole(& holePos6);

    return new_table;
}

///////////////////////////////////////////////////////////////////////////////////////////////////

phylib_object * phylib_new_hole(
        phylib_coord * pos
        )
{
    // Allocate memory for a new phylib_object
    phylib_object * new_object = calloc(1, sizeof(phylib_object));

    // If malloc fails, return NULL
    if (new_object == NULL) {
        return NULL;
    }
    memset(new_object, 0, sizeof(phylib_object));

    // Set the type to PHYLIB_HOLE
    new_object->type = PHYLIB_HOLE;

    // Transfer the information provided in the function parameters into the structure
    if (pos) {
        new_object->obj.hole.pos.x = pos->x;
        new_object->obj.hole.pos.y = pos->y;
    }

    // Return a pointer to the phylib_object
    return new_object;
}

///////////////////////////////////////////////////////////////////////////////////////////////////

phylib_object * phylib_new_hcushion(
        double y
        )
{
    // Allocate memory for a new phylib_object
    phylib_object *new_object = calloc(1, sizeof(phylib_object));

    // If malloc fails, return NULL
    if (new_object == NULL) {
        return NULL;
    }

    // Set the type to PHYLIB_HCUSHION
    new_object->type = PHYLIB_HCUSHION;

    // Transfer the information provided in the function parameters into the structure
    new_object->obj.hcushion.y = y;

    // Return a pointer to the phylib_object
    return new_object;
}

///////////////////////////////////////////////////////////////////////////////////////////////////

phylib_object * phylib_new_vcushion(
        double x
        )
{
    // Allocate memory for a new phylib_object
    phylib_object *new_object = calloc(1, sizeof(phylib_object));

    // If malloc fails, return NULL
    if (new_object == NULL) {
        return NULL;
    }

    // Set the type to PHYLIB_VCUSHION
    new_object->type = PHYLIB_VCUSHION;

    // Transfer the information provided in the function parameters into the structure
    new_object->obj.vcushion.x = x;

    // Return a pointer to the phylib_object
    return new_object;
}

///////////////////////////////////////////////////////////////////////////////////////////////////
//
///////////////////////////////////////////////////////////////////////////////////////////////////

void phylib_copy_object(
        phylib_object ** dest,
        phylib_object ** src
        )
{ // utility function 1
    if (dest == NULL) {
        //empty
    } else {
        if (src == NULL || * src == NULL) {
            * dest = NULL;
        } else {
            * dest = malloc(sizeof(phylib_object));
            // Check if memory allocation is successful
            if (* dest == NULL) {
                //empty
            } else {
                memcpy(
                        * dest,
                        * src,
                        sizeof(phylib_object)
                      );
            }
        }
    }
}

///////////////////////////////////////////////////////////////////////////////////////////////////

phylib_table * phylib_copy_table(
        phylib_table * table
        )
{ // utility function 2
    phylib_table * result;

    if (table == NULL) {
        result = NULL;
    } else {
        result = malloc(sizeof(phylib_table));

        if (result == NULL){ // malloc fail checking
            //empty
        } else {
            result->time = table->time;

            for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
                phylib_copy_object(
                        result->object+i,
                        table->object+i
                        );
            }
        }
    }
    return result;
}

///////////////////////////////////////////////////////////////////////////////////////////////////

void phylib_add_object(
        phylib_table * table,
        phylib_object * object
        )
{ // utility function 3
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] == NULL) {
            table->object[i] = object;
            break;
        }
    }
}

///////////////////////////////////////////////////////////////////////////////////////////////////

void phylib_free_table(
        phylib_table * table
        )
{ // utility function 4
    if (table) {
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            free(table->object[i]);
        }
    }
    free(table);
}

///////////////////////////////////////////////////////////////////////////////////////////////////
//
///////////////////////////////////////////////////////////////////////////////////////////////////

phylib_coord phylib_sub(
        phylib_coord c1,
        phylib_coord c2
        )
{ // utility function 5
    phylib_coord result;
    result.x = c1.x-c2.x;
    result.y = c1.y-c2.y;
    return result;
}

///////////////////////////////////////////////////////////////////////////////////////////////////

double phylib_length(phylib_coord c) { // utility function 6
    return sqrt((c.x*c.x)+(c.y*c.y));
}

///////////////////////////////////////////////////////////////////////////////////////////////////

double phylib_dot_product(phylib_coord a, phylib_coord b ) { // utility function 7
    return (a.x*b.x)+(a.y*b.y);
}

///////////////////////////////////////////////////////////////////////////////////////////////////
//
///////////////////////////////////////////////////////////////////////////////////////////////////

double phylib_distance( // utility function 8
        phylib_object * obj1,
        phylib_object * obj2
        )
{
    double result;

    if (obj1->type != PHYLIB_ROLLING_BALL) {
        result = -1.0;
    } else {
        phylib_coord diff;
        double dist;

        switch(obj2->type)
        {
            case PHYLIB_STILL_BALL:
                {
                    diff = phylib_sub(
                            obj2->obj.still_ball.pos,
                            obj1->obj.rolling_ball.pos
                            );
                    dist = phylib_length(
                            diff
                            );
                    result = dist-PHYLIB_BALL_DIAMETER;
                }
                break;
            case PHYLIB_ROLLING_BALL:
                {
                    diff = phylib_sub(
                            obj2->obj.rolling_ball.pos,
                            obj1->obj.rolling_ball.pos
                            );
                    dist = phylib_length(
                            diff
                            );
                    result = dist-PHYLIB_BALL_DIAMETER;
                }
                break;
            case PHYLIB_HOLE:
                {
                    diff = phylib_sub(
                            obj2->obj.hole.pos,
                            obj1->obj.rolling_ball.pos
                            );
                    dist = phylib_length(
                            diff
                            );
                    result = dist - PHYLIB_HOLE_RADIUS;
                }
                break;
            case PHYLIB_HCUSHION:
                {
                    result = fabs(obj1->obj.rolling_ball.pos.y-obj2->obj.hcushion.y)-PHYLIB_BALL_RADIUS;
                }
                break;
            case PHYLIB_VCUSHION:
                {
                    result = fabs(obj1->obj.rolling_ball.pos.x-obj2->obj.vcushion.x)-PHYLIB_BALL_RADIUS;
                }
                break;
            default:
                result = -1.0;
                break;
        }
    }
    return result;
}

///////////////////////////////////////////////////////////////////////////////////////////////////
//
///////////////////////////////////////////////////////////////////////////////////////////////////

// PART 3 FUNCTION IMPLEMENTATION FROM HERE

void phylib_roll(
        phylib_object * new,
        phylib_object * old,
        double time
        )
{
    if (new == NULL || old == NULL) {
        //empty
    } else if (new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL) {
        //empty
    } else {
        phylib_rolling_ball * vaOld = & old->obj.rolling_ball;
        phylib_rolling_ball * vaNew = & new->obj.rolling_ball;

        // p = p1 + (v1 * t) + (1/2 * a1 * t^2)

        vaNew->pos.x = 0
            + vaOld->pos.x
            + (vaOld->vel.x*time)
            + (0.5*vaOld->acc.x*time*time)
            ;
        vaNew->pos.y = 0
            + vaOld->pos.y
            + (vaOld->vel.y*time)
            + (0.5*vaOld->acc.y*time*time)
            ;

        // v = v1 + (a1 * t)

        vaNew->vel.x = vaOld->vel.x+(vaOld->acc.x*time);
        vaNew->vel.y = vaOld->vel.y+(vaOld->acc.y*time);

        if ((vaOld->vel.x > 0 && vaNew->vel.x < 0) || (vaOld->vel.x < 0 && vaNew->vel.x > 0)) {
            vaNew->vel.x = 0;
            vaNew->acc.x = 0;
        }
        if ((vaOld->vel.y > 0 && vaNew->vel.y < 0) || (vaOld->vel.y < 0 && vaNew->vel.y > 0)) {
            vaNew->vel.y = 0;
            vaNew->acc.y = 0;
        }
    }
}

///////////////////////////////////////////////////////////////////////////////////////////////////

unsigned char phylib_stopped(
        phylib_object * object
        )
{
    unsigned char result;

    // assert(object && object->type == PHYLIB_ROLLING_BALL);

    // Calculate the speed of the ball

    phylib_rolling_ball * ptr = & object->obj.rolling_ball;

    double speed = sqrt(
            ptr->vel.x*ptr->vel.x
            +
            ptr->vel.y*ptr->vel.y
            );

    // Checking the speed is less than PHYLIB_VEL_EPSILON

    if (speed < PHYLIB_VEL_EPSILON) {

        // Convert the rolling ball to a still ball

        // make a temporary copy of the existing value

        phylib_rolling_ball tmp;

        memcpy(
                & tmp,
                ptr,
                sizeof(phylib_rolling_ball)
              );

        object->obj.still_ball.number = tmp.number;
        object->obj.still_ball.pos.x = tmp.pos.x;
        object->obj.still_ball.pos.y = tmp.pos.y;
        object->type = PHYLIB_STILL_BALL;

        result = 1;
    } else {
        result = 0;
    }
    return result;
}

///////////////////////////////////////////////////////////////////////////////////////////////////

void phylib_bounce(
        phylib_object ** a,
        phylib_object ** b
        )
{
    // assert(a && a->type == PHYLIB_ROLLING_BALL);

    if (b == NULL) {
        //empty
    } else {
        phylib_rolling_ball * ptrA = & (* a)->obj.rolling_ball;

        switch((* b)->type)
        {
            case PHYLIB_HCUSHION:
                {
                    ptrA->vel.y = -ptrA->vel.y;
                    ptrA->acc.y = -ptrA->acc.y;
                }
                break;
            case PHYLIB_VCUSHION:
                {
                    ptrA->vel.x = -ptrA->vel.x;
                    ptrA->acc.x = -ptrA->acc.x;
                }
                break;
            case PHYLIB_HOLE:
                {
                    free(* a);

                    * a = NULL;
                }
                break;
            case PHYLIB_STILL_BALL:
                {
                    phylib_object * tmp = phylib_new_rolling_ball(
                            (* b)->obj.still_ball.number,
                            & (* b)->obj.still_ball.pos,
                            NULL,
                            NULL
                            );
                    if (tmp) {
                        free(* b);

                        * b = tmp;
                    } else {
                        // no memory, abort

                        break;
                    }
                }
                // break;
            case PHYLIB_ROLLING_BALL:
                {
                    phylib_rolling_ball * ptrB = & (* b)->obj.rolling_ball;

                    phylib_coord r_ab = phylib_sub(
                            ptrA->pos,
                            ptrB->pos
                            );

                    phylib_coord v_rel = phylib_sub(
                            ptrA->vel,
                            ptrB->vel
                            );

                    double r_ab_len = phylib_length(
                            r_ab
                            );

                    phylib_coord n = {
                        DIV(r_ab.x, r_ab_len),
                        DIV(r_ab.y, r_ab_len)
                    };

                    double v_rel_n = phylib_dot_product(
                            v_rel,
                            n
                            );

                    ptrA->vel.x -= v_rel_n*n.x;
                    ptrA->vel.y -= v_rel_n*n.y;

                    ptrB->vel.x += v_rel_n*n.x;
                    ptrB->vel.y += v_rel_n*n.y;

                    double speed_a = phylib_length(
                            ptrA->vel
                            );
                    double speed_b = phylib_length(
                            ptrB->vel
                            );

                    if (speed_a > PHYLIB_VEL_EPSILON) {
                        ptrA->acc.x = ((-ptrA->vel.x)/speed_a)*PHYLIB_DRAG;
                        ptrA->acc.y = ((-ptrA->vel.y)/speed_a)*PHYLIB_DRAG;
                    }
                    if (speed_b > PHYLIB_VEL_EPSILON) {
                        ptrB->acc.x = ((-ptrB->vel.x)/speed_b)*PHYLIB_DRAG;
                        ptrB->acc.y = ((-ptrB->vel.y)/speed_b)*PHYLIB_DRAG;
                    }
                }
                break;
            default:
                break;
        }
    }
}

///////////////////////////////////////////////////////////////////////////////////////////////////

unsigned char phylib_rolling(
        phylib_table * t
        )
{
    unsigned char result = 0;

    if (t) {
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            if (t->object[i] != NULL && (t->object[i]->type == PHYLIB_ROLLING_BALL)) {
                result++;
            }
        }
    }
    return result;
}

///////////////////////////////////////////////////////////////////////////////////////////////////

phylib_table * phylib_segment(
        phylib_table * table
        )
{
    phylib_table * result;

    if (phylib_rolling(table) == 0) {
        result = NULL;
    } else {
        result = phylib_copy_table(
                table
                );
        double time = 0;

        phylib_object * ptr;

        while (1) {
            if (time >= PHYLIB_MAX_TIME) {
                break;
            } else {
                // check for one stopped ball

                for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
                    ptr = result->object[i];

                    if (ptr == NULL) {
                        //empty
                    } else if (ptr->type == PHYLIB_ROLLING_BALL) {
                        unsigned char eqStop = phylib_stopped(
                                ptr
                                );

                        if (eqStop) {
                            goto lbl_end;
                        }
                    } else {
                        //empty
                    }
                }

                // increase time after roll

                time += PHYLIB_SIM_RATE;

                // let the balls roll

                for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
                    ptr = result->object[i];

                    if (ptr == NULL) {
                        //empty
                    } else if (ptr->type == PHYLIB_ROLLING_BALL) {
                        phylib_roll(
                                ptr,
                                table->object[i],
                                time
                                );
                    } else {
                        //empty
                    }
                }

                // check for distance

                for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
                    ptr = result->object[i];

                    if (ptr == NULL) {
                        //empty
                    } else if (ptr->type == PHYLIB_ROLLING_BALL) {

                        for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
                            if (i == j) {
                                continue;
                            }
                            phylib_object * ptrOther = result->object[j];

                            if (ptrOther == NULL) {
                                //empty
                            } else {
                                double dist = phylib_distance(
                                        ptr,
                                        ptrOther
                                        );

                                if (dist < 0.0) {
                                    phylib_bounce(
                                            & ptr,
                                            & ptrOther
                                            );

                                    result->object[i] = ptr;
                                    result->object[j] = ptrOther;

                                    time -= PHYLIB_SIM_RATE;

                                    goto lbl_end;
                                }
                            }
                        }

                    } else {
                        //empty
                    }
                }
            }
        }
lbl_end:
        ;
        result->time += time;
    }
    return result;
}
char *phylib_object_string( phylib_object *object )
{
        static char string[80];
        if (object==NULL)
        {
        snprintf( string, 80, "NULL;" );
        return string;
        }
        switch (object->type)
        {
        case PHYLIB_STILL_BALL:
        snprintf( string, 80,
        "STILL_BALL (%d,%6.1lf,%6.1lf)",
        object->obj.still_ball.number,
        object->obj.still_ball.pos.x,
        object->obj.still_ball.pos.y );
        break;
        case PHYLIB_ROLLING_BALL:
        snprintf( string, 80,
        "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
        object->obj.rolling_ball.number,
        object->obj.rolling_ball.pos.x,
        object->obj.rolling_ball.pos.y,
        object->obj.rolling_ball.vel.x,
        object->obj.rolling_ball.vel.y,
        object->obj.rolling_ball.acc.x,
        object->obj.rolling_ball.acc.y );
        break;
        case PHYLIB_HOLE:
        snprintf( string, 80,
        "HOLE (%6.1lf,%6.1lf)",
        object->obj.hole.pos.x,
        object->obj.hole.pos.y );
        break;
        case PHYLIB_HCUSHION:
        snprintf( string, 80,
        "HCUSHION (%6.1lf)",
        object->obj.hcushion.y );
        break;
        case PHYLIB_VCUSHION:
        snprintf( string, 80,
        "VCUSHION (%6.1lf)",
        object->obj.vcushion.x );
        break;
        }
        return string;
    }

    
///////////////////////////////////////////////////////////////////////////////////////////////////
//
///////////////////////////////////////////////////////////////////////////////////////////////////
