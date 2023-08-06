//Ortec CHN File format
//
#define BUILDING_XYLIB
#include "ortec_chn.h"

#include <ctime>
#include <cstring>

#include "util.h"

using namespace std;
using namespace xylib::util;

namespace xylib {


const FormatInfo OrtecChnDataSet::fmt_info(
    "ortec_chn",
    "Ortec CHN",
    "chn",
    true,                       // whether binary
    false,                      // whether has multi-blocks
    &OrtecChnDataSet::ctor,
    &OrtecChnDataSet::check
);

bool OrtecChnDataSet::check(istream &f, string*)
{
    int header = read_uint16_le(f);
    return header == 65535;
}
static string get_month(string month){
    if(month=="Jan") return "1";
    if(month=="Feb") return "2";
    if(month=="Mar") return "3";
    if(month=="Apr") return "4";
    if(month=="May") return "5";
    if(month=="Jun") return "6";
    if(month=="Jul") return "7";
    if(month=="Aug") return "8";
    if(month=="Sep") return "9";
    if(month=="Oct") return "10";
    if(month=="Nov") return "11";
    if(month=="Dec") return "12";
    return "";
}
void OrtecChnDataSet::load_data(std::istream &f, const char*)
{

    AutoPtrBlock blk(new Block);
    Column *xcol = NULL;
    VecColumn *ycol = new VecColumn;

    f.seekg(0, f.beg);

    f.ignore(6);
    string sec = read_string(f, 2);
    float livetime = (float)read_uint32_le(f);
    float realtime = (float)read_uint32_le(f);
    blk->meta["live time (s)"] = std::to_string(livetime);
    blk->meta["real time (s)"] = std::to_string(realtime);

    string day = read_string(f, 2);
    string month = read_string(f, 3);

    string year = read_string(f, 2);
    int millenium = read_uint8_le(f) & 1;
    if(millenium){
        year = "20" + year;
    }
    else{
        year = "19" + year;
    }

    string hr = read_string(f, 2);
    string min = read_string(f, 2);
    blk->meta["Start Time"] = year + "-" + get_month(month) + "-" + day + " " + hr + ":" + min + ":" + sec;

    int offset = read_uint16_le(f);
    //channel count
    int count = read_uint16_le(f);

    f.ignore(offset*4);
    for(int i=0;i<count;i++){
        int y = read_uint32_le(f);
        ycol->add_val(y);
        if(f.eof()){
            throw FormatError("Could not find all channels in file");
        }
    }

    int flag = read_int16_le(f);
    while(flag != -102 && flag != -101 && ! f.eof()){
        flag = read_int16_le(f);
    }

    if(f.eof()){
        throw FormatError("Could not find footer block");
    }

    if(flag == -102){
        f.ignore(2);
        float e_int = read_flt_le(f);
        float e_slope = read_flt_le(f);
        float e_quadr = read_flt_le(f);
        if(e_quadr == 0.0F){
            xcol = new StepColumn(e_int, e_slope, count);
        }
        else{
            VecColumn *vc = new VecColumn;
            for(int i=0;i<count;i++){
                vc->add_val(e_quadr*i*i + e_slope*i + e_int);
            }
            xcol = vc;
        }
    }
    else if(flag==-101){
        f.ignore(6);
        float e_int = read_flt_le(f);
        float e_slope = read_flt_le(f);
        xcol = new StepColumn(e_int, e_slope, count);
    }

    blk->add_column(xcol);
    blk->add_column(ycol);
    add_block(blk.release());
}
}// namespace xylib