from optparse import OptionParser

"""
Scoring Metrics for KDD Cup 2012, Track 2

Reads in a solution/subission files

Scores on the following three metrics:
-NWMAE
-WRMSE
-AUC

Author: Ben Hamner (kdd2012@benhamner.com)
"""


def scoreElementwiseMetric(num_clicks, num_impressions, predicted_ctr, elementwise_metric):
    """
    Calculates an elementwise error metric

    Parameters
    ----------
    num_clicks : a list containing the number of clicks

    num_impressions : a list containing the number of impressions

    predicted_ctr : a list containing the predicted click-through rates

    elementwise_metric : a function such as MSE that evaluates the error on a single instance, given the clicks, impressions, and p_ctr

    Returns
    -------
    score : the error on the elementwise metric over the set
    """
    score = 0.0
    weight_sum = 0.0

    for clicks, impressions, p_ctr in zip(num_clicks, num_impressions, predicted_ctr):
        score += elementwise_metric(clicks, impressions, p_ctr) * impressions
        weight_sum += impressions
    score /= weight_sum
    return score


def scoreWRMSE(num_clicks, num_impressions, predicted_ctr):
    """
    Calculates the Weighted Root Mean Squared Error (WRMSE)

    Parameters
    ----------
    num_clicks : a list containing the number of clicks

    num_impressions : a list containing the number of impressions

    predicted_ctr : a list containing the predicted click-through rates

    Returns
    -------
    wrmse : the weighted root mean squared error
    """
    import math

    mse = lambda clicks, impressions, p_ctr: math.pow(clicks / impressions - p_ctr, 2.0)
    wmse = scoreElementwiseMetric(num_clicks, num_impressions, predicted_ctr, mse)
    wrmse = math.sqrt(wmse)
    return wrmse


def scoreNWMAE(num_clicks, num_impressions, predicted_ctr):
    """
    Calculates the normalized weighted mean absolute error

    Parameters
    ----------
    num_clicks : a list containing the number of clicks

    num_impressions : a list containing the number of impressions

    predicted_ctr : a list containing the predicted click-through rates

    Returns
    -------
    nwmae : the normalized weighted mean absolute error
    """
    mae = lambda clicks, impressions, p_ctr: abs(clicks / impressions - p_ctr)
    nwmae = scoreElementwiseMetric(num_clicks, num_impressions, predicted_ctr, mae)
    return nwmae


def scoreClickAUC(num_clicks, num_impressions, predicted_ctr):
    """
    Calculates the area under the ROC curve (AUC) for click rates

    Parameters
    ----------
    num_clicks : a list containing the number of clicks

    num_impressions : a list containing the number of impressions

    predicted_ctr : a list containing the predicted click-through rates

    Returns
    -------
    auc : the area under the ROC curve (AUC) for click rates
    """
    i_sorted = sorted(range(len(predicted_ctr)), key=lambda i: predicted_ctr[i],
                      reverse=True)
    auc_temp = 0.0
    click_sum = 0.0
    old_click_sum = 0.0
    no_click = 0.0
    no_click_sum = 0.0

    # treat all instances with the same predicted_ctr as coming from the
    # same bucket
    last_ctr = predicted_ctr[i_sorted[0]] + 1.0

    for i in xrange(len(predicted_ctr)):
        if last_ctr != predicted_ctr[i_sorted[i]]:
            auc_temp += (click_sum + old_click_sum) * no_click / 2.0
            old_click_sum = click_sum
            no_click = 0.0
            last_ctr = predicted_ctr[i_sorted[i]]
        no_click += num_impressions[i_sorted[i]] - num_clicks[i_sorted[i]]
        no_click_sum += num_impressions[i_sorted[i]] - num_clicks[i_sorted[i]]
        click_sum += num_clicks[i_sorted[i]]
    auc_temp += (click_sum + old_click_sum) * no_click / 2.0
    auc = auc_temp / (click_sum * no_click_sum)
    return auc


def bucket_predictions(num_clicks, num_impressions, predicted_ctr, num_digits=4):
    predicted_ctr_buckets = {}

    for clicks, impressions, p_ctr in zip(num_clicks, num_impressions, predicted_ctr):
        p_ctr = round(p_ctr, num_digits)
        if p_ctr not in predicted_ctr_buckets:
            predicted_ctr_buckets[p_ctr] = [0, 0]
        predicted_ctr_buckets[p_ctr][0] += clicks
        predicted_ctr_buckets[p_ctr][1] += impressions
    predicted_ctr_b = sorted(predicted_ctr_buckets.keys())
    num_clicks_b = []
    num_impressions_b = []
    for p_ctr in predicted_ctr_b:
        num_clicks_b.append(predicted_ctr_buckets[p_ctr][0])
        num_impressions_b.append(predicted_ctr_buckets[p_ctr][1])
    return num_clicks_b, num_impressions_b, predicted_ctr_b


def bucket_predictions_quantiles(num_clicks, num_impressions, predicted_ctr, num_quantiles=50):
    i_sorted = sorted(range(len(predicted_ctr)), key=lambda i: predicted_ctr[i],
                      reverse=True)
    num_clicks_q = []
    num_impressions_q = []
    predicted_ctr_q = []

    clicks = 0
    impressions = 0
    p_clicks = 0

    for i in range(len(i_sorted)):
        clicks += num_clicks[i_sorted[i]]
        impressions += num_impressions[i_sorted[i]]
        p_clicks += predicted_ctr[i_sorted[i]] * num_impressions[i_sorted[i]]

        if i % int(len(num_clicks) / num_quantiles) == 0 or i == len(i_sorted) - 1:
            num_clicks_q.append(clicks)
            num_impressions_q.append(impressions)
            predicted_ctr_q.append(p_clicks / impressions)

            clicks = 0
            impressions = 0
            p_clicks = 0

    return num_clicks_q, num_impressions_q, predicted_ctr_q


def read_solution_file(f_sol_name, delimiter=','):
    """
    Reads in a solution file

    Parameters
    ----------
    f_sol_name : submission file name

    Returns
    -------
    num_clicks : a list of clicks
    num_impressions : a list of impressions
    """
    f_sol = open(f_sol_name)

    num_clicks = []
    num_impressions = []
    types = []

    for line in f_sol:
        line = line.strip().split(delimiter)
        try:
            clicks = float(line[0])
            impressions = float(line[1])
            instance_type = line[2]
        except ValueError:
            # skip over header
            continue
        num_clicks.append(clicks)
        num_impressions.append(impressions)
        types.append(instance_type)
    return num_clicks, num_impressions, types


def read_submission_file(f_sub_name, delimiter=','):
    """
    Reads in a submission file

    Parameters
    ----------
    f_sub_name : submission file name

    Returns
    -------
    predicted_ctr : a list of predicted click-through rates
    """
    f_sub = open(f_sub_name)

    predicted_ctr = []

    for line in f_sub:
        line = line.strip().split(delimiter)
        predicted_ctr.append(float(line[0]))

    return predicted_ctr


def main():
    optparser = OptionParser(usage="""
    %prog [OPTIONS] SOLUTION_FILE SUBMISSION_FILE""")
    optparser.add_option('-f', '--filter', dest='filter',
                         type='string', default=None,
                         help='Calc only on public or private data')
    optparser.add_option('-d', '--delimiter', dest='delimiter',
                         type='string', default=',',
                         help='File columns delimiter')
    opts, args = optparser.parse_args()

    solution_file = args[0]
    submission_file = args[1]

    num_clicks, num_impressions, types = read_solution_file(solution_file, opts.delimiter)
    predicted_ctr = read_submission_file(submission_file, opts.delimiter)
    if opts.filter is not None:
        num_clicks = [num_clicks[i] for i in xrange(len(num_clicks)) if types[i] == opts.filter]
        num_impressions = [num_impressions[i] for i in xrange(len(num_impressions)) if types[i] == opts.filter]
        predicted_ctr = [predicted_ctr[i] for i in xrange(len(predicted_ctr)) if types[i] == opts.filter]

    auc = scoreClickAUC(num_clicks, num_impressions, predicted_ctr)
    print("AUC  : %f" % auc)
    nwmae = scoreNWMAE(num_clicks, num_impressions, predicted_ctr)
    print("NWMAE: %f" % nwmae)
    wrmse = scoreWRMSE(num_clicks, num_impressions, predicted_ctr)
    print("WRMSE: %f" % wrmse)

if __name__ == "__main__":
    main()
