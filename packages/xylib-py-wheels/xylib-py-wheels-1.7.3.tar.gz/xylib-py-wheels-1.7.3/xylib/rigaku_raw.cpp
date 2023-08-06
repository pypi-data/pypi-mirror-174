//Rigaku RAW file format
//
#define BUILDING_XYLIB
#include "rigaku_raw.h"

#include <ctime>
#include <cstring>

#include "util.h"

using namespace std;
using namespace xylib::util;

namespace xylib {


const FormatInfo RigakuRawDataSet::fmt_info(
    "rigaku_raw",
    "Rigaku RAW",
    "raw",
    true,                       // whether binary
    true,                      // whether has multi-blocks
    &RigakuRawDataSet::ctor,
    &RigakuRawDataSet::check
);

bool RigakuRawDataSet::check(istream &f, string*)
{
    string head = read_string(f, 2);
    return head == "FI";//File Info? - CS
}

static
string get_time(int t){
    time_t rawtime = (time_t)t;
    char s[64];
    int r = strftime(s, sizeof(s), "%a, %Y-%m-%d %H:%M:%S", gmtime(&rawtime));
    return s;
}

void RigakuRawDataSet::load_data(std::istream &f, const char*)
{

    f.seekg(0, f.beg);
    f.ignore(4);
    int c = read_uint8_le(f);

    if(c==216){
        f.ignore(1207);
        //Wavelengths 1 and 2
        float alpha1 = (float)read_dbl_le(f);
        meta["Wavelength 1"] = std::to_string(alpha1);
        float alpha2 = (float)read_dbl_le(f);
        meta["Wavelength 2"] = std::to_string(alpha2);

        while(!f.eof()){
            if(read_char(f) == 'P' && !f.eof() && read_char(f) == 'I'){ //PI = Partition Info?? - CS
                AutoPtrBlock blk(new Block);
                Column *xcol = NULL;
                VecColumn *ycol = new VecColumn;
                f.ignore(28);

                //These appear to be UNIX start and end times
                int start_time = read_int32_le(f);
                blk->meta["Start Time"] = get_time(start_time);
                int end_time = read_int32_le(f);
                blk->meta["End Time"] = get_time(end_time);

                f.ignore(788);
                float start = read_flt_le(f);
                float cur_pos = start;
                float stop = read_flt_le(f);
                float step = read_flt_le(f);
                double dcount = (stop - start) / step + 1;
                int count = iround(dcount);
                xcol = new StepColumn(start, step, count);
                while(!f.eof()){
                    if(read_char(f) == 'D' && !f.eof() && read_char(f) == 'A'){
                        f.ignore(18);
                        for(int i=1;i<count;i++){
                            cur_pos = cur_pos + step;
                            if(f.eof()){
                                break;
                            }
                            float y = read_flt_le(f);
                            ycol->add_val(y);
                        }
                        blk->add_column(xcol);
                        blk->add_column(ycol);
                        add_block(blk.release());
                    }
                }
            }
        }
    }
    else{
        AutoPtrBlock blk(new Block);
        Column *xcol = NULL;
        VecColumn *ycol = new VecColumn;

        f.ignore(979);

        //Wavelengths 1 and 2
        float alpha1 = (float)read_dbl_le(f);
        blk->meta["Wavelength 1"] = std::to_string(alpha1);
        float alpha2 = (float)read_dbl_le(f);
        blk->meta["Wavelength 2"] = std::to_string(alpha2);

        //I didn't have any files with the 5th byte set like this, so I couldn't find the timestamps or properly implement multiblock - CS

        f.ignore(2004);

        float start = read_flt_le(f);
        float cur_pos = start;
        float stop = read_flt_le(f);
        float step = read_flt_le(f);
        double dcount = (stop - start) / step + 1;
        int count = iround(dcount);
        xcol = new StepColumn(start, step, count);

        f.ignore(42);

        for(int i=0;i<count;i++){
            cur_pos = cur_pos + step;
            if(cur_pos > stop || f.eof()){
                break;
            }
            float y = read_flt_le(f);
            ycol->add_val(y);
        }

        blk->add_column(xcol);
        blk->add_column(ycol);
        add_block(blk.release());
    }
    
} 
}// namespace xylib