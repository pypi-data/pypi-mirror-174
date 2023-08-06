//Ortec CHN File format
//
#define BUILDING_XYLIB
#include "ortec_spc.h"

#include <ctime>
#include <cstring>

#include "util.h"

using namespace std;
using namespace xylib::util;

namespace xylib {


const FormatInfo OrtecSpcDataSet::fmt_info(
    "ortec_spc",
    "Ortec SPC",
    "spc",
    true,                       // whether binary
    false,                      // whether has multi-blocks
    &OrtecSpcDataSet::ctor,
    &OrtecSpcDataSet::check
);

bool OrtecSpcDataSet::check(istream &f, string*)
{
    return read_uint16_le(f) == 1 && (read_uint16_le(f) >> 3) == 0;
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
}
static string get_date(std::istream &f){
    string day = read_string(f, 2);
    string month = read_string(f, 3);
    string year = read_string(f, 2);
    string time = read_string(f, 8);
    int millenium = read_uint8_le(f) & 1;
    if(millenium){
        year = "20" + year;
    }
    else{
        year = "19" + year;
    }
    return year + "-" + get_month(month) + "-" + day + " " + time;
}
void OrtecSpcDataSet::load_data(std::istream &f, const char*)
{
    AutoPtrBlock blk(new Block);
    Column *xcol = NULL;
    VecColumn *ycol = new VecColumn;

    f.seekg(0, f.beg);
    f.ignore(2);
    int type = read_uint16_le(f);
    int isReal = (type >> 2) & 1;
    int longFilename = read_uint16_le(f) >> 15;
    uint16_t pointers[17];

    for(int i=0;i<16;i++){
        pointers[i] = read_uint16_le(f);
    }
    f.ignore(12);
    pointers[16] = read_uint16_le(f);
    
    f.ignore(6);
    int spectrumPointer = read_uint16_le(f);
    int numRecords = read_uint16_le(f);
    int numChannels = read_uint16_le(f);
    f.ignore(20);
    int startChannel = read_uint16_le(f);

    float realtime = read_flt_le(f);
    float livetime = read_flt_le(f);
    blk->meta["real time (s)"] = to_string(realtime);
    blk->meta["live time (s)"] = to_string(realtime);

    //Acquisition info
    f.seekg((pointers[0]-1)*128, f.beg);
    blk->meta["Spectrum Name"] = read_string(f, 16);
    f.ignore(74);

    blk->meta["Start Time"] = get_date(f);
    blk->meta["End Time"] = get_date(f);

    //Sample info
    f.seekg((pointers[1]-1)*128, f.beg);
    blk->meta["Sample Description"] = read_string(f, 128);

    //Detector Info
    f.seekg((pointers[2]-1)*128, f.beg);
    blk->meta["Detector Description"] = read_string(f, 128);

    //Energy Callibration
    f.seekg((pointers[13]-1)*128, f.beg);
    f.ignore(20);
    float e_quadr = read_flt_le(f);
    float e_slope = read_flt_le(f);
    float e_int = read_flt_le(f);
    if(e_quadr == 0){
        xcol = new StepColumn(e_int, e_slope, numChannels);
    }
    else{
        VecColumn *vc = new VecColumn;
        for(int i=0;i<numChannels;i++){
            vc->add_val(e_quadr * i * i + e_slope * i + e_int);
        }
        xcol = vc;
    }
    //Loads more metadata stored in this filetype, but harder to extract/less relavant IMO (Potential TODO) - CS

    //Spectrum Data
    f.seekg((spectrumPointer-1)*128, f.beg);
    if(isReal){
        for(int i=0;i<numChannels;i++){
            ycol->add_val(read_flt_le(f));
        }
    }
    else{
        for(int i=0;i<numChannels;i++){
            ycol->add_val(read_uint32_le(f));
        }
    }
} 
}// namespace xylib