/*
Start with http://simplestatistics.org/
ISC License 
*/

function max(x /*: Array<number> */) /*:number*/ {
    var value;
    for (var i = 0; i < x.length; i++) {
        if (value === undefined || x[i] > value) {
            value = x[i];
        }
    }
    if (value === undefined) {
        return NaN;
    }
    return value;
}

function min(x /*: Array<number> */)/*:number*/ {
    var value;
    for (var i = 0; i < x.length; i++) {
        if (value === undefined || x[i] < value) {
            value = x[i];
        }
    }
    if (value === undefined) {
        return NaN;
    }
    return value;
}

function sum(x/*: Array<number> */)/*: number */ {
    var sum = 0;
    var errorCompensation = 0;
    var correctedCurrentValue;
    var nextSum;
    for (var i = 0; i < x.length; i++) {
        correctedCurrentValue = x[i] - errorCompensation;
        nextSum = sum + correctedCurrentValue;
        errorCompensation = nextSum - sum - correctedCurrentValue;
        sum = nextSum;
    }
    return sum;
}

function mean(x /*: Array<number> */)/*:number*/ {
    if (x.length === 0) { return NaN; }
    return sum(x) / x.length;
}

function sumNthPowerDeviations(x/*: Array<number> */, n/*: number */)/*:number*/ {
    var meanValue = mean(x),
        sum = 0;

    for (var i = 0; i < x.length; i++) {
        sum += Math.pow(x[i] - meanValue, n);
    }

    return sum;
}

function variance(x/*: Array<number> */)/*:number*/ {
    if (x.length === 0) { return NaN; }

    return sumNthPowerDeviations(x, 2) / x.length;
}

function standardDeviation(x /*: Array<number> */)/*:number*/ {
    var v = variance(x);
    if (isNaN(v)) { return 0; }
    return Math.sqrt(v);
}

function sampleStandardDeviation(x/*:Array<number>*/)/*:number*/ {
    var sampleVarianceX = sampleVariance(x);
    if (isNaN(sampleVarianceX)) { return NaN; }
    return Math.sqrt(sampleVarianceX);
}

function sampleVariance(x /*: Array<number> */)/*:number*/ {
    if (x.length <= 1) { return NaN; }

    var sumSquaredDeviationsValue = sumNthPowerDeviations(x, 2);
    var besselsCorrection = x.length - 1;
    return sumSquaredDeviationsValue / besselsCorrection;
}

function sampleCovariance(x /*:Array<number>*/, y /*:Array<number>*/)/*:number*/ {
    if (x.length <= 1 || x.length !== y.length) {
        return NaN;
    }

    var xmean = mean(x),
        ymean = mean(y),
        sum = 0;

    for (var i = 0; i < x.length; i++) {
        sum += (x[i] - xmean) * (y[i] - ymean);
    }
    var besselsCorrection = x.length - 1;
    return sum / besselsCorrection;
}

function sampleCorrelation(x/*: Array<number> */, y/*: Array<number> */)/*:number*/ {
    var cov = sampleCovariance(x, y),
        xstd = sampleStandardDeviation(x),
        ystd = sampleStandardDeviation(y);

    return cov / xstd / ystd;
}

/*

My statistics function

*/

function standardize(arr){
	var avg = mean(arr);
	var stdev = standardDeviation(arr);
	r_arr = []
	for(var idx = 0; idx < arr.length; idx++){
		r_arr.push((arr[idx]-avg)/stdev);
	}
	return r_arr;
}

function featureScaling(arr){
	var amax = max(arr);
	var amin = min(arr);
	r_arr = []
	for(var idx = 0; idx < arr.length; idx++){
		r_arr.push((arr[idx]-amin)/(amax-amin));
	}
	return r_arr;

}
